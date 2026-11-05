"""
farmer_profiles.py
==================
Farmer Profile Management module for Person 3 backend.
Implements secure profile creation, retrieval, updates, and searching.

Data Privacy Enforcement:
- Rejects any attempted storage of raw 12-digit Aadhaar numbers or document scans.
- Tracks document availability strictly as boolean flags / document name lists.
- Enforces mandatory consent prior to profile persistence.
- Enforces uniqueness of farmer_id to prevent duplicates.
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from person3.farmer_database import connect, init_db
from person3.consent_manager import validate_consent


def _sanitize_and_validate_privacy(profile: Dict[str, Any]):
    """
    Ensure no raw Aadhaar numbers (12-digit patterns) or document binaries
    are injected into the prototype.
    """
    for key, value in profile.items():
        if "aadhaar_number" in key.lower() or "uid" in key.lower():
            if value and re.search(r"\b\d{12}\b", str(value)):
                raise ValueError(
                    "Privacy Violation: Storing raw 12-digit Aadhaar numbers is strictly "
                    "prohibited in this prototype. Only store document readiness flags."
                )
        if isinstance(value, str) and (value.startswith("data:image") or len(value) > 5000):
            raise ValueError(
                f"Privacy Violation: Storing raw document file content in field '{key}' "
                "is prohibited. Only store document presence status."
            )


def _normalize_profile_input(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize input field names supporting both hackathon aliases and canonical names:
    - farmer_name / name
    - phone_number / phone
    - preferred_language / language
    - intermediary_id
    - consent_status / consent
    - uploaded_documents / documents
    - bank_account_name / bank_name
    """
    farmer_id = profile.get("farmer_id")
    if not farmer_id or not str(farmer_id).strip():
        raise ValueError("farmer_id is a required field.")

    farmer_name = profile.get("farmer_name") or profile.get("name")
    if not farmer_name or not str(farmer_name).strip():
        raise ValueError("farmer_name is a required field.")

    # Validate consent
    consent = profile.get("consent_status")
    if consent is None:
        consent = profile.get("consent")
    validate_consent(consent)

    phone_number = profile.get("phone_number") or profile.get("phone") or ""
    language = profile.get("preferred_language") or profile.get("language") or "Telugu"
    intermediary_id = profile.get("intermediary_id") or None
    bank_account_name = profile.get("bank_account_name") or profile.get("bank_name") or ""

    # Normalize documents
    docs = profile.get("uploaded_documents")
    if docs is None:
        docs = profile.get("documents")
    if docs is None:
        docs = {}
    elif isinstance(docs, list):
        # Convert list of docs to dict {doc_name: True}
        docs = {doc: True for doc in docs}

    return {
        "farmer_id": str(farmer_id).strip(),
        "farmer_name": str(farmer_name).strip(),
        "phone_number": str(phone_number).strip(),
        "preferred_language": str(language).strip(),
        "intermediary_id": str(intermediary_id).strip() if intermediary_id else None,
        "consent_status": 1,
        "uploaded_documents": docs,
        "bank_account_name": str(bank_account_name).strip() if bank_account_name else None,
    }


def _format_profile_output(row: Any) -> Dict[str, Any]:
    """
    Convert SQLite row into a rich profile dictionary with canonical and alias keys
    for maximum compatibility with Person 1 and Person 2 modules.
    """
    data = dict(row)
    doc_json = data.pop("uploaded_documents", "{}")
    try:
        documents = json.loads(doc_json)
    except Exception:
        documents = {}

    farmer_id = data["farmer_id"]
    farmer_name = data["farmer_name"]
    phone_number = data["phone_number"]
    language = data["preferred_language"]
    intermediary_id = data["intermediary_id"]
    consent_bool = bool(data["consent_status"])
    bank_account_name = data["bank_account_name"]
    created_at = data["created_at"]

    return {
        # Canonical keys
        "farmer_id": farmer_id,
        "farmer_name": farmer_name,
        "phone_number": phone_number,
        "preferred_language": language,
        "intermediary_id": intermediary_id,
        "consent_status": consent_bool,
        "uploaded_documents": documents,
        "bank_account_name": bank_account_name,
        "created_at": created_at,
        # Team compatibility aliases
        "name": farmer_name,
        "phone": phone_number,
        "language": language,
        "consent": consent_bool,
        "documents": documents,
        "bank_name": bank_account_name,
    }


def save_profile(profile: Dict[str, Any], db_path=None) -> Dict[str, Any]:
    """
    Register a new farmer profile.
    Automatically creates database if not present.
    Prevents duplicate farmer IDs (raises ValueError).
    """
    init_db(db_path)
    _sanitize_and_validate_privacy(profile)
    normalized = _normalize_profile_input(profile)

    with connect(db_path) as con:
        # Check for duplicate farmer_id
        existing = con.execute(
            "SELECT farmer_id FROM farmers WHERE farmer_id = ?",
            (normalized["farmer_id"],)
        ).fetchone()

        if existing:
            raise ValueError(
                f"Farmer ID '{normalized['farmer_id']}' already exists. "
                "Duplicate IDs are not permitted. Use update_profile() to update details."
            )

        created_at = datetime.now().isoformat(timespec="seconds")
        con.execute("""
            INSERT INTO farmers (
                farmer_id, farmer_name, phone_number, preferred_language,
                intermediary_id, consent_status, uploaded_documents,
                bank_account_name, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            normalized["farmer_id"],
            normalized["farmer_name"],
            normalized["phone_number"],
            normalized["preferred_language"],
            normalized["intermediary_id"],
            normalized["consent_status"],
            json.dumps(normalized["uploaded_documents"]),
            normalized["bank_account_name"],
            created_at,
        ))
        con.commit()

    return get_profile(normalized["farmer_id"], db_path=db_path)


def get_profile(farmer_id: str, db_path=None) -> Optional[Dict[str, Any]]:
    """
    Retrieve farmer profile by unique farmer_id.
    Returns formatted dictionary or None if not found.
    """
    init_db(db_path)
    with connect(db_path) as con:
        row = con.execute(
            "SELECT * FROM farmers WHERE farmer_id = ?",
            (str(farmer_id).strip(),)
        ).fetchone()

    if not row:
        return None
    return _format_profile_output(row)


def search_farmer(farmer_id: str, db_path=None) -> Optional[Dict[str, Any]]:
    """
    Search farmer by farmer_id. Returns profile if found, else None.
    """
    return get_profile(farmer_id, db_path=db_path)


def update_profile(farmer_id: str, updated_data: Dict[str, Any], db_path=None) -> Dict[str, Any]:
    """
    Update details for an existing farmer profile.
    Raises ValueError if farmer does not exist.
    """
    init_db(db_path)
    _sanitize_and_validate_privacy(updated_data)
    farmer_id_clean = str(farmer_id).strip()

    current_profile = get_profile(farmer_id_clean, db_path=db_path)
    if not current_profile:
        raise ValueError(f"Farmer with ID '{farmer_id_clean}' not found.")

    # Merge incoming updates
    name = (
        updated_data.get("farmer_name")
        or updated_data.get("name")
        or current_profile["farmer_name"]
    )
    phone = (
        updated_data.get("phone_number")
        if "phone_number" in updated_data
        else updated_data.get("phone", current_profile["phone_number"])
    )
    language = (
        updated_data.get("preferred_language")
        or updated_data.get("language")
        or current_profile["preferred_language"]
    )
    intermediary_id = (
        updated_data.get("intermediary_id")
        if "intermediary_id" in updated_data
        else current_profile["intermediary_id"]
    )

    consent_val = updated_data.get("consent_status")
    if consent_val is None:
        consent_val = updated_data.get("consent")
    if consent_val is not None:
        consent_int = 1 if (consent_val is True or consent_val == 1) else 0
    else:
        consent_int = 1 if current_profile["consent_status"] else 0

    docs = updated_data.get("uploaded_documents")
    if docs is None:
        docs = updated_data.get("documents")
    if docs is not None:
        if isinstance(docs, list):
            docs = {doc: True for doc in docs}
    else:
        docs = current_profile["uploaded_documents"]

    bank_name = (
        updated_data.get("bank_account_name")
        if "bank_account_name" in updated_data
        else updated_data.get("bank_name", current_profile["bank_account_name"])
    )

    with connect(db_path) as con:
        con.execute("""
            UPDATE farmers SET
                farmer_name = ?,
                phone_number = ?,
                preferred_language = ?,
                intermediary_id = ?,
                consent_status = ?,
                uploaded_documents = ?,
                bank_account_name = ?
            WHERE farmer_id = ?
        """, (
            str(name).strip(),
            str(phone).strip(),
            str(language).strip(),
            str(intermediary_id).strip() if intermediary_id else None,
            consent_int,
            json.dumps(docs),
            str(bank_name).strip() if bank_name else None,
            farmer_id_clean,
        ))
        con.commit()

    return get_profile(farmer_id_clean, db_path=db_path)


def list_all_farmers(db_path=None, active_consent_only=False) -> List[Dict[str, Any]]:
    """
    List all farmers in the database.
    """
    init_db(db_path)
    with connect(db_path) as con:
        query = "SELECT * FROM farmers"
        if active_consent_only:
            query += " WHERE consent_status = 1"
        query += " ORDER BY farmer_name ASC"
        rows = con.execute(query).fetchall()

    return [_format_profile_output(r) for r in rows]
