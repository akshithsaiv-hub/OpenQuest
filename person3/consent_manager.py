"""
consent_manager.py
==================
Consent management module for Person 3 backend.
Ensures explicit, informed consent is tracked, validated, and retractable.

Compliance & Transparency:
- Mandatory explicit opt-in before saving any farmer profile.
- Explicit purpose disclosure: data is used solely for scheme eligibility,
  application guidance, and deadline reminders.
- Immediate withdrawal mechanism that stops notifications and hides profile
  from intermediary view.
- Tracks consent language, purpose codes, and timestamps.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from person3.farmer_database import connect
from security.audit_service import log_runtime_audit_event

CONSENT_PURPOSE_STATEMENT = (
    "I consent to the collection and processing of my profile details solely "
    "for agricultural scheme eligibility evaluation, document readiness checking, "
    "and receiving timely deadline reminders. I understand that I can withdraw "
    "my consent at any time, which will immediately cease all reminders and "
    "hide my information from intermediary dashboards."
)


def get_consent_terms() -> dict:
    """
    Return human-readable consent terms and purpose notice for UI presentation.
    """
    return {
        "title": "Farmer Information Consent",
        "purpose": CONSENT_PURPOSE_STATEMENT,
        "purpose_codes": ["scheme_matching", "document_verification", "reminders"],
        "data_collected": [
            "Farmer ID (Unique Identifier)",
            "Farmer Name & Bank Account Name (for mismatch verification)",
            "Contact Phone & Preferred Language",
            "Document Availability Flags (NO raw Aadhaar numbers or copies stored)",
            "CSC/FPO Intermediary ID (if registered via facilitator)"
        ],
        "rights": "You may view, correct, export, or withdraw consent at any time."
    }


def validate_consent(consent_value) -> bool:
    """
    Validate that consent is strictly True or 1.
    Raises ValueError with explanatory message if consent is not granted.
    """
    if consent_value is True or consent_value == 1:
        return True
    raise ValueError(
        "Consent is required before saving a profile. "
        "The farmer must agree to the data usage terms for scheme assistance."
    )


def withdraw_consent(farmer_id: str, db_path=None, actor_id: Optional[str] = None) -> bool:
    """
    Withdraw consent for a farmer.
    Once withdrawn:
    - Reminders are stopped immediately.
    - Profile is excluded from intermediary views.
    Returns True if successfully updated, False if farmer_id not found.
    """
    farmer_id_str = str(farmer_id).strip()
    with connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE farmers SET consent_status = 0 WHERE farmer_id = ? AND is_deleted = 0",
            (farmer_id_str,)
        )
        con.commit()
        if cur.rowcount == 0:
            return False

    log_runtime_audit_event(
        action_type="CONSENT_REVOKE",
        target_resource="farmer_consent",
        record_id=farmer_id_str,
        actor_id=actor_id or farmer_id_str,
        actor_role="farmer",
        db_path=db_path
    )
    return True


def grant_consent(
    farmer_id: str,
    language_code: str = "en",
    purpose: str = "scheme_matching,reminders",
    db_path=None,
    actor_id: Optional[str] = None
) -> bool:
    """
    Re-activate consent for a farmer if they re-opt in.
    """
    farmer_id_str = str(farmer_id).strip()
    now_iso = datetime.now().isoformat(timespec="seconds")
    with connect(db_path) as con:
        cur = con.cursor()
        cur.execute("""
            UPDATE farmers SET 
                consent_status = 1,
                consent_language = ?,
                consent_purpose = ?,
                consent_timestamp = ?
            WHERE farmer_id = ? AND is_deleted = 0
        """, (language_code, purpose, now_iso, farmer_id_str))
        con.commit()
        if cur.rowcount == 0:
            return False

    log_runtime_audit_event(
        action_type="CONSENT_GRANT",
        target_resource="farmer_consent",
        record_id=farmer_id_str,
        actor_id=actor_id or farmer_id_str,
        actor_role="farmer",
        db_path=db_path
    )
    return True


def is_consent_active(farmer_id: str, db_path=None) -> bool:
    """
    Check if a farmer has active consent and is not soft-deleted.
    """
    farmer_id_str = str(farmer_id).strip()
    with connect(db_path) as con:
        row = con.execute(
            "SELECT consent_status, is_deleted FROM farmers WHERE farmer_id = ?",
            (farmer_id_str,)
        ).fetchone()
        if not row:
            return False
        if row["is_deleted"] == 1:
            return False
        return bool(row["consent_status"])


def get_consent_record(farmer_id: str, db_path=None) -> Optional[Dict[str, Any]]:
    """
    Retrieve full consent metadata for a farmer.
    """
    farmer_id_str = str(farmer_id).strip()
    with connect(db_path) as con:
        row = con.execute("""
            SELECT farmer_id, consent_status, consent_language, consent_purpose,
                   consent_timestamp, is_deleted
            FROM farmers WHERE farmer_id = ?
        """, (farmer_id_str,)).fetchone()
        if not row:
            return None
        return dict(row)
