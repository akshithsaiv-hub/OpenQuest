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
"""

from datetime import datetime
from typing import Optional
from person3.farmer_database import connect

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
        "data_collected": [
            "Farmer ID (Unique Identifier)",
            "Farmer Name & Bank Account Name (for mismatch verification)",
            "Contact Phone & Preferred Language",
            "Document Availability Flags (NO Aadhaar numbers or copies stored)",
            "CSC/FPO Intermediary ID (if registered via facilitator)"
        ],
        "rights": "You may withdraw consent at any time via phone, CSC center, or online portal."
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


def withdraw_consent(farmer_id: str, db_path=None) -> bool:
    """
    Withdraw consent for a farmer.
    Once withdrawn:
    - Reminders are stopped.
    - Profile is excluded from intermediary views.
    Returns True if successfully updated, False if farmer_id not found.
    """
    farmer_id_str = str(farmer_id).strip()
    with connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE farmers SET consent_status = 0 WHERE farmer_id = ?",
            (farmer_id_str,)
        )
        con.commit()
        if cur.rowcount == 0:
            return False
        return True


def grant_consent(farmer_id: str, db_path=None) -> bool:
    """
    Re-activate consent for a farmer if they re-opt in.
    """
    farmer_id_str = str(farmer_id).strip()
    with connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE farmers SET consent_status = 1 WHERE farmer_id = ?",
            (farmer_id_str,)
        )
        con.commit()
        return cur.rowcount > 0


def is_consent_active(farmer_id: str, db_path=None) -> bool:
    """
    Check if a farmer has active consent.
    """
    farmer_id_str = str(farmer_id).strip()
    with connect(db_path) as con:
        row = con.execute(
            "SELECT consent_status FROM farmers WHERE farmer_id = ?",
            (farmer_id_str,)
        ).fetchone()
        if not row:
            return False
        return bool(row["consent_status"])
