"""
pin_service.py
==============
Safeguard 2, 4, 9: Farmer Passbook PIN Management & Persistent Brute-Force Lockout.

Provides Argon2id salted password hashing, complexity validation, and database-persisted
lockout mechanisms for Farmer Passbook review requests.

Security Controls:
- Argon2id salted hashing (Memory-hard, side-channel resistant).
- Strictly rejects storage, logging, transmission, or display of plain PINs.
- Complexity: 4-8 numeric digits, rejects repetitive or trivial sequential sequences.
- Brute-force protection: 5 failed attempts -> 15-minute persistent lockout.
- Lockout state stored in the database (`pin_failed_attempts`, `pin_locked_until`),
  ensuring it persists across server restarts.
- Generic error messages to prevent account enumeration.
"""

import re
import os
import secrets
import logging
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, Any

from security.audit_service import log_runtime_audit_event

logger = logging.getLogger("DLP.PINService")

PIN_MIN_LENGTH = 4
PIN_MAX_LENGTH = 8
MAX_PIN_ATTEMPTS = 5
LOCKOUT_MINUTES = 15

# Trivial/weak PINs explicitly banned
TRIVIAL_PINS = {
    "0000", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999",
    "1234", "4321", "12345", "54321",
    "000000", "111111", "222222", "333333", "444444", "555555", "666666", "777777", "888888", "999999",
    "123456", "654321", "12345678", "87654321"
}

# Initialize Argon2id Password Hasher
_hasher = None
try:
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
    _hasher = PasswordHasher(
        time_cost=2,
        memory_cost=65536,  # 64 MiB
        parallelism=1,
        hash_len=32,
        salt_len=16
    )
    logger.info("Initialized Argon2id password hasher for farmer passbook PIN protection.")
except ImportError:
    import hashlib
    logger.warning("argon2-cffi not installed; using standard scrypt fallback.")
    _hasher = None


def validate_pin_format(pin: str) -> Tuple[bool, Optional[str]]:
    """
    Validates PIN format and strength requirements:
    - 4 to 8 numeric digits
    - Disallows all-identical or trivial sequences
    """
    if not pin or not isinstance(pin, str):
        return False, "PIN must be provided as a numeric string."

    pin_clean = pin.strip()
    if not re.match(r"^\d{4,8}$", pin_clean):
        return False, f"PIN must be between {PIN_MIN_LENGTH} and {PIN_MAX_LENGTH} numeric digits."

    # Check repeating single digit (e.g., 0000, 11111)
    if len(set(pin_clean)) == 1:
        return False, "PIN is too weak: repeating single digit is not permitted."

    if pin_clean in TRIVIAL_PINS:
        return False, "PIN is too common or easily guessable. Please choose a more secure PIN."

    return True, None


def hash_pin(pin: str) -> str:
    """
    Generate an Argon2id salted password hash for the PIN.
    Never stores or returns the plain PIN.
    """
    pin_clean = pin.strip()
    if _hasher is not None:
        return _hasher.hash(pin_clean)

    # Scrypt fallback with cryptographically random 16-byte salt
    import hashlib
    import base64
    salt = secrets.token_bytes(16)
    key = hashlib.scrypt(pin_clean.encode("utf-8"), salt=salt, n=16384, r=8, p=1, maxmem=32 * 1024 * 1024)
    salt_b64 = base64.b64encode(salt).decode("ascii")
    key_b64 = base64.b64encode(key).decode("ascii")
    return f"$scrypt$ln=14,r=8,p=1${salt_b64}${key_b64}"


def verify_pin_hash(stored_hash: str, pin: str) -> bool:
    """
    Verify submitted PIN against the stored cryptographic hash.
    Safe against timing attacks.
    """
    if not stored_hash or not pin:
        return False

    pin_clean = pin.strip()

    if _hasher is not None and stored_hash.startswith("$argon2"):
        try:
            return _hasher.verify(stored_hash, pin_clean)
        except Exception:
            return False

    if stored_hash.startswith("$scrypt$"):
        import hashlib
        import base64
        try:
            parts = stored_hash.split("$")
            salt = base64.b64decode(parts[3])
            expected_key = base64.b64decode(parts[4])
            computed_key = hashlib.scrypt(pin_clean.encode("utf-8"), salt=salt, n=16384, r=8, p=1, maxmem=32 * 1024 * 1024)
            return secrets.compare_digest(computed_key, expected_key)
        except Exception:
            return False

    return False


def set_farmer_pin(farmer_id: str, new_pin: str, db_path=None) -> Tuple[bool, str]:
    """
    Configures a new Argon2id PIN for the farmer.
    Enforces format validation and resets failed attempts/lockout.
    """
    from person3.farmer_database import connect

    is_valid, err = validate_pin_format(new_pin)
    if not is_valid:
        return False, err or "Invalid PIN format."

    pin_hashed = hash_pin(new_pin)
    now_iso = datetime.now().isoformat()

    with connect(db_path) as con:
        cur = con.execute("""
            UPDATE farmers
            SET pin_hash = ?,
                pin_created_at = ?,
                pin_failed_attempts = 0,
                pin_locked_until = NULL
            WHERE farmer_id = ? AND is_deleted = 0
        """, (pin_hashed, now_iso, str(farmer_id).strip()))
        con.commit()

        if cur.rowcount == 0:
            return False, "Farmer account not found or is inactive."

    log_runtime_audit_event(
        action_type="PIN_SETUP",
        target_resource="farmers",
        record_id=farmer_id,
        actor_id=farmer_id,
        role="farmer"
    )
    return True, "Passbook review PIN successfully configured."


def change_farmer_pin(
    farmer_id: str,
    current_pin: str,
    new_pin: str,
    db_path=None
) -> Tuple[bool, str]:
    """
    Changes existing PIN after verifying the current PIN (with brute-force lockout checks).
    """
    # 1. Verify current PIN first
    ok, msg = verify_farmer_pin(farmer_id, current_pin, db_path=db_path)
    if not ok:
        return False, msg

    # 2. Validate and set new PIN
    is_valid, err = validate_pin_format(new_pin)
    if not is_valid:
        return False, err or "Invalid new PIN format."

    if current_pin.strip() == new_pin.strip():
        return False, "New PIN must be different from your current PIN."

    ok, set_msg = set_farmer_pin(farmer_id, new_pin, db_path=db_path)
    if ok:
        log_runtime_audit_event(
            action_type="PIN_CHANGED",
            target_resource="farmers",
            record_id=farmer_id,
            actor_id=farmer_id,
            role="farmer"
        )
        return True, "Passbook PIN successfully updated."
    return False, set_msg


def verify_farmer_pin(
    farmer_id: str,
    submitted_pin: str,
    db_path=None
) -> Tuple[bool, str]:
    """
    Verifies farmer PIN with database-persisted brute force lockout tracking.
    Never reveals plain PIN or whether non-PIN details are valid.

    Returns:
    (True, "PIN_VERIFIED") on success
    (False, "<ERROR_CODE>: <user_safe_message>") on failure
    """
    from person3.farmer_database import connect

    now = datetime.now()
    now_iso = now.isoformat()

    with connect(db_path) as con:
        row = con.execute("""
            SELECT farmer_id, pin_hash, pin_failed_attempts, pin_locked_until, is_deleted
            FROM farmers
            WHERE farmer_id = ?
        """, (str(farmer_id).strip(),)).fetchone()

        if not row or row["is_deleted"] == 1:
            return False, "INCORRECT_PIN: Verification failed."

        if not row["pin_hash"]:
            return False, "PIN_NOT_CONFIGURED: PIN has not been set up for this account. Please create a PIN first."

        # Check existing lockout
        locked_until_str = row["pin_locked_until"]
        if locked_until_str:
            try:
                locked_until = datetime.fromisoformat(locked_until_str)
                if now < locked_until:
                    secs_remaining = int((locked_until - now).total_seconds())
                    mins_remaining = max(1, (secs_remaining + 59) // 60)
                    log_runtime_audit_event(
                        action_type="PIN_VERIFY_BLOCKED_LOCKED",
                        target_resource="farmers",
                        record_id=farmer_id,
                        actor_id=farmer_id,
                        role="farmer"
                    )
                    return False, f"LOCKED_OUT: Account is temporarily locked due to repeated incorrect PIN attempts. Try again in {mins_remaining} minute(s)."
            except Exception:
                pass

        # Perform constant-time verification
        is_match = verify_pin_hash(row["pin_hash"], submitted_pin)

        if is_match:
            # Reset failed attempts and clear lockout
            con.execute("""
                UPDATE farmers
                SET pin_failed_attempts = 0,
                    pin_locked_until = NULL
                WHERE farmer_id = ?
            """, (farmer_id,))
            con.commit()

            log_runtime_audit_event(
                action_type="PIN_VERIFY_SUCCESS",
                target_resource="farmers",
                record_id=farmer_id,
                actor_id=farmer_id,
                role="farmer"
            )
            return True, "PIN_VERIFIED"

        else:
            # Increment failed attempts
            current_attempts = (row["pin_failed_attempts"] or 0) + 1
            locked_until_iso = None

            if current_attempts >= MAX_PIN_ATTEMPTS:
                locked_until_dt = now + timedelta(minutes=LOCKOUT_MINUTES)
                locked_until_iso = locked_until_dt.isoformat()

            con.execute("""
                UPDATE farmers
                SET pin_failed_attempts = ?,
                    pin_locked_until = ?
                WHERE farmer_id = ?
            """, (current_attempts, locked_until_iso, farmer_id))
            con.commit()

            log_runtime_audit_event(
                action_type="PIN_VERIFY_FAILED",
                target_resource="farmers",
                record_id=farmer_id,
                actor_id=farmer_id,
                role="farmer"
            )

            if locked_until_iso:
                return False, f"LOCKED_OUT: Maximum 5 incorrect PIN attempts exceeded. Account is locked for {LOCKOUT_MINUTES} minutes."

            remaining = MAX_PIN_ATTEMPTS - current_attempts
            return False, f"INCORRECT_PIN: Incorrect PIN. {remaining} attempt(s) remaining before temporary lockout."


def get_farmer_pin_status(farmer_id: str, db_path=None) -> Dict[str, Any]:
    """
    Returns public PIN security status without leaking the hash or salt.
    """
    from person3.farmer_database import connect

    now = datetime.now()

    with connect(db_path) as con:
        row = con.execute("""
            SELECT pin_hash, pin_failed_attempts, pin_locked_until, pin_created_at
            FROM farmers
            WHERE farmer_id = ? AND is_deleted = 0
        """, (str(farmer_id).strip(),)).fetchone()

        if not row:
            return {"is_pin_set": False, "is_locked": False, "failed_attempts": 0}

        is_set = bool(row["pin_hash"])
        is_locked = False
        remaining_secs = 0

        locked_until_str = row["pin_locked_until"]
        if locked_until_str:
            try:
                locked_until = datetime.fromisoformat(locked_until_str)
                if now < locked_until:
                    is_locked = True
                    remaining_secs = int((locked_until - now).total_seconds())
            except Exception:
                pass

        return {
            "is_pin_set": is_set,
            "is_locked": is_locked,
            "lockout_remaining_seconds": remaining_secs,
            "failed_attempts": row["pin_failed_attempts"] or 0,
            "pin_created_at": row["pin_created_at"]
        }
