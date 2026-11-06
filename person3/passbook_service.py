"""
passbook_service.py
===================
Passbook Document Wallet Service (Single-Document Scope & Review Protection).

Capabilities:
- Scope: Exclusively manages the Farmer Bank Passbook / DBT Mandate.
- Full CRUD: Upload, View, Replace, Delete passbook metadata.
- Clear state tracking: Saved status, upload timestamp, review status.
- PIN-guarded review requests: Verifies Argon2id PIN and explicit consent before submission.
- Role-based reviewer access: Only authorized officers/intermediaries with active farmer consent
  can access passbooks that have been submitted for review.
- Audit logging for all operations.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

from security.pin_service import verify_farmer_pin, get_farmer_pin_status
from security.audit_service import log_runtime_audit_event
from security.validators import validate_no_pii_leakage

logger = logging.getLogger("DLP.PassbookService")


def mask_account_number(acc: str) -> str:
    """Mask account number to display only the last 4 digits."""
    clean = re_digits = "".join(filter(str.isdigit, str(acc)))
    if len(clean) >= 4:
        return f"******{clean[-4:]}"
    return "******"


def get_farmer_passbook(farmer_id: str, db_path=None) -> Dict[str, Any]:
    """
    Retrieves the farmer's passbook record and review status.
    Excludes sensitive raw information and PIN hashes.
    """
    from person3.farmer_database import connect

    with connect(db_path) as con:
        row = con.execute("""
            SELECT farmer_id, farmer_name, bank_account_name,
                   passbook_saved, passbook_filename, passbook_uploaded_at,
                   passbook_data, passbook_review_status, passbook_reviewed_at,
                   passbook_reviewer_id, consent_status, is_deleted
            FROM farmers
            WHERE farmer_id = ? AND is_deleted = 0
        """, (str(farmer_id).strip(),)).fetchone()

        if not row:
            return {
                "farmer_id": farmer_id,
                "is_saved": False,
                "review_status": "not_uploaded",
                "message": "Farmer record not found."
            }

        pin_status = get_farmer_pin_status(farmer_id, db_path=db_path)

        is_saved = bool(row["passbook_saved"])
        raw_data = {}
        if is_saved and row["passbook_data"]:
            try:
                raw_data = json.loads(row["passbook_data"])
            except Exception:
                raw_data = {}

        return {
            "farmer_id": farmer_id,
            "farmer_name": row["farmer_name"],
            "is_saved": is_saved,
            "uploaded_at": row["passbook_uploaded_at"],
            "filename": row["passbook_filename"] or ("passbook_scan.svg" if is_saved else None),
            "review_status": row["passbook_review_status"] or "not_requested",
            "reviewed_at": row["passbook_reviewed_at"],
            "reviewer_id": row["passbook_reviewer_id"],
            "passbook_details": raw_data,
            "pin_configured": pin_status["is_pin_set"],
            "pin_locked": pin_status["is_locked"],
            "lockout_remaining_seconds": pin_status.get("lockout_remaining_seconds", 0)
        }


def save_or_replace_passbook(
    farmer_id: str,
    passbook_payload: Dict[str, Any],
    db_path=None
) -> Dict[str, Any]:
    """
    Upload or replace a farmer passbook.
    Enforces data minimization (masks account number, validates no raw PII leaks).
    """
    from person3.farmer_database import connect

    # Validate data minimization
    validate_no_pii_leakage(passbook_payload)

    bank_name = str(passbook_payload.get("bank_name", "State Bank of India")).strip()
    branch = str(passbook_payload.get("branch", "Main Branch")).strip()
    account_holder = str(passbook_payload.get("account_holder_name", "")).strip()
    raw_acc = str(passbook_payload.get("account_number", "")).strip()
    ifsc = str(passbook_payload.get("ifsc", "SBIN0020144")).strip().upper()
    dbt_seeded = bool(passbook_payload.get("npci_dbt_seeded", True))

    masked_acc = mask_account_number(raw_acc) if raw_acc else "******3492"

    sanitized_data = {
        "document_type": "bank_passbook",
        "title": f"{bank_name} Passbook / DBT Mandate",
        "bank_name": bank_name,
        "branch": branch,
        "account_holder_name": account_holder,
        "account_number_masked": masked_acc,
        "ifsc_code": ifsc,
        "npci_dbt_seeded": dbt_seeded,
        "sample_preview_uri": "samples/sample_passbook.svg",
    }

    now_iso = datetime.now().isoformat()
    json_blob = json.dumps(sanitized_data)

    with connect(db_path) as con:
        # Check if passbook was already saved
        existing = con.execute(
            "SELECT passbook_saved FROM farmers WHERE farmer_id = ? AND is_deleted = 0",
            (farmer_id,)
        ).fetchone()

        if not existing:
            raise ValueError(f"Farmer '{farmer_id}' does not exist or has been deleted.")

        action_type = "PASSBOOK_REPLACE" if existing["passbook_saved"] else "PASSBOOK_UPLOAD"

        con.execute("""
            UPDATE farmers
            SET passbook_saved = 1,
                passbook_filename = ?,
                passbook_uploaded_at = ?,
                passbook_data = ?,
                passbook_review_status = 'not_requested',
                bank_account_name = COALESCE(NULLIF(?, ''), bank_account_name)
            WHERE farmer_id = ? AND is_deleted = 0
        """, ("passbook_scan.svg", now_iso, json_blob, account_holder, farmer_id))
        con.commit()

    log_runtime_audit_event(
        action_type=action_type,
        target_resource="passbooks",
        record_id=farmer_id,
        actor_id=farmer_id,
        role="farmer"
    )

    return {
        "status": "success",
        "message": "Farmer passbook saved successfully.",
        "is_saved": True,
        "uploaded_at": now_iso,
        "passbook_details": sanitized_data
    }


def delete_farmer_passbook(farmer_id: str, db_path=None) -> bool:
    """
    Deletes the saved passbook record and resets review status.
    """
    from person3.farmer_database import connect

    with connect(db_path) as con:
        cur = con.execute("""
            UPDATE farmers
            SET passbook_saved = 0,
                passbook_filename = NULL,
                passbook_uploaded_at = NULL,
                passbook_data = NULL,
                passbook_review_status = 'not_requested',
                passbook_reviewed_at = NULL,
                passbook_reviewer_id = NULL
            WHERE farmer_id = ? AND is_deleted = 0
        """, (farmer_id,))
        con.commit()

        if cur.rowcount == 0:
            return False

    log_runtime_audit_event(
        action_type="PASSBOOK_DELETE",
        target_resource="passbooks",
        record_id=farmer_id,
        actor_id=farmer_id,
        role="farmer"
    )
    return True


def request_passbook_review(
    farmer_id: str,
    submitted_pin: str,
    consent_to_share: bool,
    notes: Optional[str] = None,
    db_path=None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    PIN-protected passbook review request workflow:
    1. Verify explicit consent to share with reviewer.
    2. Verify passbook exists.
    3. Verify PIN with persistent brute-force lockout.
    4. Transition status to 'pending_review' upon success.
    """
    from person3.farmer_database import connect

    # 1. Check explicit consent
    if not consent_to_share:
        return False, "CONSENT_REQUIRED: Explicit farmer consent is mandatory before submitting passbook for review.", None

    # 2. Check passbook exists
    with connect(db_path) as con:
        row = con.execute("""
            SELECT farmer_id, passbook_saved, passbook_review_status, consent_status, is_deleted
            FROM farmers
            WHERE farmer_id = ? AND is_deleted = 0
        """, (farmer_id,)).fetchone()

        if not row:
            return False, "ACCOUNT_NOT_FOUND: Farmer account not found or deleted.", None

        if not row["passbook_saved"]:
            return False, "PASSBOOK_MISSING: No passbook is saved. Please upload your passbook before requesting review.", None

    # 3. Verify PIN with lockout protection
    pin_ok, pin_msg = verify_farmer_pin(farmer_id, submitted_pin, db_path=db_path)
    if not pin_ok:
        return False, pin_msg, None

    # 4. Mark review requested
    now_iso = datetime.now().isoformat()
    with connect(db_path) as con:
        con.execute("""
            UPDATE farmers
            SET passbook_review_status = 'pending_review'
            WHERE farmer_id = ? AND is_deleted = 0
        """, (farmer_id,))
        con.commit()

    log_runtime_audit_event(
        action_type="PASSBOOK_REVIEW_REQUESTED",
        target_resource="passbooks",
        record_id=farmer_id,
        actor_id=farmer_id,
        role="farmer"
    )

    return True, "Passbook review requested successfully.", {
        "farmer_id": farmer_id,
        "review_status": "pending_review",
        "requested_at": now_iso
    }


def get_passbook_for_reviewer(
    farmer_id: str,
    reviewer_id: str,
    reviewer_role: str,
    db_path=None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Authorized access for field officers or CSC intermediaries to review a farmer's passbook.
    Strictly checks:
    - Farmer has active consent (consent_status = 1 AND is_deleted = 0)
    - Review has been requested (passbook_review_status in ('pending_review', 'under_review', 'verified'))
    - If reviewer is intermediary, farmer must be assigned to them.
    """
    from person3.farmer_database import connect

    with connect(db_path) as con:
        row = con.execute("""
            SELECT farmer_id, farmer_name, intermediary_id, consent_status, is_deleted,
                   passbook_saved, passbook_filename, passbook_uploaded_at, passbook_data,
                   passbook_review_status, passbook_reviewed_at, passbook_reviewer_id
            FROM farmers
            WHERE farmer_id = ?
        """, (farmer_id,)).fetchone()

        if not row or row["is_deleted"] == 1:
            return False, "NOT_FOUND: Farmer record not found or has been deleted.", None

        if row["consent_status"] != 1:
            return False, "CONSENT_WITHDRAWN: Access denied. Farmer has withdrawn consent.", None

        if not row["passbook_saved"]:
            return False, "NO_PASSBOOK: No passbook has been uploaded for this farmer.", None

        # Verify review was actually requested
        status = row["passbook_review_status"] or "not_requested"
        if status in ("not_requested", "rejected"):
            return False, f"REVIEW_NOT_REQUESTED: Farmer has not submitted passbook for review (status: '{status}').", None

        # If intermediary, ensure farmer is assigned to this intermediary
        if reviewer_role == "intermediary":
            if row["intermediary_id"] != reviewer_id:
                return False, "UNAUTHORIZED_INTERMEDIARY: This farmer is not assigned to your CSC center.", None

        # Update status to under_review if currently pending
        if status == "pending_review":
            con.execute("""
                UPDATE farmers
                SET passbook_review_status = 'under_review',
                    passbook_reviewer_id = ?
                WHERE farmer_id = ?
            """, (reviewer_id, farmer_id))
            con.commit()

    log_runtime_audit_event(
        action_type="PASSBOOK_REVIEW_ACCESSED",
        target_resource="passbooks",
        record_id=farmer_id,
        actor_id=reviewer_id,
        role=reviewer_role
    )

    passbook_details = {}
    if row["passbook_data"]:
        try:
            passbook_details = json.loads(row["passbook_data"])
        except Exception:
            pass

    return True, "Success", {
        "farmer_id": row["farmer_id"],
        "farmer_name": row["farmer_name"],
        "intermediary_id": row["intermediary_id"],
        "review_status": "under_review" if status == "pending_review" else status,
        "uploaded_at": row["passbook_uploaded_at"],
        "passbook_details": passbook_details
    }


def record_reviewer_decision(
    farmer_id: str,
    reviewer_id: str,
    decision: str,  # "verified" or "rejected"
    notes: Optional[str] = None,
    db_path=None
) -> Tuple[bool, str]:
    """
    Officer records verification or rejection decision on submitted passbook.
    """
    from person3.farmer_database import connect

    clean_decision = decision.lower().strip()
    if clean_decision not in ("verified", "rejected"):
        return False, "Decision must be 'verified' or 'rejected'."

    now_iso = datetime.now().isoformat()
    with connect(db_path) as con:
        cur = con.execute("""
            UPDATE farmers
            SET passbook_review_status = ?,
                passbook_reviewed_at = ?,
                passbook_reviewer_id = ?
            WHERE farmer_id = ? AND is_deleted = 0
        """, (clean_decision, now_iso, reviewer_id, farmer_id))
        con.commit()

        if cur.rowcount == 0:
            return False, "Farmer not found or deleted."

    log_runtime_audit_event(
        action_type=f"PASSBOOK_REVIEW_{clean_decision.upper()}",
        target_resource="passbooks",
        record_id=farmer_id,
        actor_id=reviewer_id,
        role="officer"
    )

    return True, f"Passbook review status updated to '{clean_decision}'."
