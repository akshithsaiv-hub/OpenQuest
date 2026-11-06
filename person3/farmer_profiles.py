"""
farmer_profiles.py
==================
Farmer Profile Management module for Person 3 backend.
Implements secure profile creation, retrieval, updates, soft-deletion, and exporting.

Data Privacy Enforcement:
- Rejects any attempted storage of raw 12-digit Aadhaar numbers or document scans.
- Enforces strict input validation across all fields.
- Tracks document availability strictly as boolean flags / document name lists.
- Enforces mandatory consent prior to profile persistence with purpose and timestamp.
- Audits profile lifecycle events without storing sensitive payloads in audit logs.
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from person3.farmer_database import connect, init_db
from person3.consent_manager import validate_consent
from security.validators import validate_no_pii_leakage, DataMinimizationViolation
from security.audit_service import log_runtime_audit_event


def _sanitize_and_validate_privacy(profile: Dict[str, Any]):
    """
    Ensure no raw Aadhaar numbers (12-digit patterns), PAN cards, or document binaries
    are admitted into the application profile storage.
    """
    validate_no_pii_leakage(profile, path="farmer_profile")


def _normalize_profile_input(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize input field names supporting canonical names and aliases.
    Validates explicit consent and captures metadata.
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
    language = profile.get("preferred_language") or profile.get("language") or "en"
    intermediary_id = profile.get("intermediary_id") or None
    bank_account_name = profile.get("bank_account_name") or profile.get("bank_name") or ""
    
    consent_lang = profile.get("consent_language") or language or "en"
    consent_purpose = profile.get("consent_purpose") or "scheme_matching,reminders"
    consent_ts = profile.get("consent_timestamp") or datetime.now().isoformat(timespec="seconds")

    state = profile.get("state") or "Telangana"
    district = profile.get("district") or "Warangal"
    crop = profile.get("crop") or "Paddy"
    land_acres = float(profile.get("land_acres") or profile.get("land_holding_acres") or 2.0)
    farmer_type = profile.get("farmer_type") or ("tenant_registered" if profile.get("is_tenant") else "owner")

    # Normalize documents
    docs = profile.get("uploaded_documents")
    if docs is None:
        docs = profile.get("documents")
    if docs is None:
        docs = {}
    elif isinstance(docs, list):
        docs = {doc: True for doc in docs}

    return {
        "farmer_id": str(farmer_id).strip(),
        "farmer_name": str(farmer_name).strip(),
        "phone_number": str(phone_number).strip(),
        "preferred_language": str(language).strip(),
        "intermediary_id": str(intermediary_id).strip() if intermediary_id else None,
        "consent_status": 1,
        "consent_language": str(consent_lang).strip(),
        "consent_purpose": str(consent_purpose).strip(),
        "consent_timestamp": str(consent_ts).strip(),
        "uploaded_documents": docs,
        "bank_account_name": str(bank_account_name).strip() if bank_account_name else None,
        "state": str(state).strip(),
        "district": str(district).strip(),
        "crop": str(crop).strip(),
        "land_acres": land_acres,
        "farmer_type": str(farmer_type).strip(),
    }


def _format_profile_output(row: Any) -> Dict[str, Any]:
    """
    Convert SQLite row into a rich profile dictionary with canonical and alias keys.
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
    is_deleted = bool(data.get("is_deleted", 0))

    return {
        "farmer_id": farmer_id,
        "farmer_name": farmer_name,
        "phone_number": phone_number,
        "preferred_language": language,
        "intermediary_id": intermediary_id,
        "consent_status": consent_bool,
        "consent_language": data.get("consent_language", "en"),
        "consent_purpose": data.get("consent_purpose", "scheme_matching,reminders"),
        "consent_timestamp": data.get("consent_timestamp", created_at),
        "is_deleted": is_deleted,
        "uploaded_documents": documents,
        "bank_account_name": bank_account_name,
        "state": data.get("state", "Telangana"),
        "district": data.get("district", "Warangal"),
        "crop": data.get("crop", "Paddy"),
        "land_acres": data.get("land_acres", 2.0),
        "farmer_type": data.get("farmer_type", "owner"),
        "created_at": created_at,
        # Team compatibility aliases
        "name": farmer_name,
        "phone": phone_number,
        "language": language,
        "consent": consent_bool,
        "documents": documents,
        "bank_name": bank_account_name,
    }


def save_profile(profile: Dict[str, Any], db_path=None, actor_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Register a new farmer profile.
    Prevents duplicate farmer IDs and audits creation.
    """
    init_db(db_path)
    _sanitize_and_validate_privacy(profile)
    normalized = _normalize_profile_input(profile)

    with connect(db_path) as con:
        existing = con.execute(
            "SELECT farmer_id, is_deleted FROM farmers WHERE farmer_id = ?",
            (normalized["farmer_id"],)
        ).fetchone()

        if existing and existing["is_deleted"] == 0:
            raise ValueError(
                f"Farmer ID '{normalized['farmer_id']}' already exists. "
                "Duplicate IDs are not permitted. Use update_profile() to update details."
            )

        created_at = datetime.now().isoformat(timespec="seconds")
        if existing and existing["is_deleted"] == 1:
            # Overwrite previously deleted account
            con.execute("""
                UPDATE farmers SET
                    farmer_name = ?, phone_number = ?, preferred_language = ?,
                    intermediary_id = ?, consent_status = 1, consent_language = ?,
                    consent_purpose = ?, consent_timestamp = ?, is_deleted = 0,
                    uploaded_documents = ?, bank_account_name = ?, state = ?,
                    district = ?, crop = ?, land_acres = ?, farmer_type = ?,
                    created_at = ?
                WHERE farmer_id = ?
            """, (
                normalized["farmer_name"], normalized["phone_number"],
                normalized["preferred_language"], normalized["intermediary_id"],
                normalized["consent_language"], normalized["consent_purpose"],
                normalized["consent_timestamp"], json.dumps(normalized["uploaded_documents"]),
                normalized["bank_account_name"], normalized["state"],
                normalized["district"], normalized["crop"],
                normalized["land_acres"], normalized["farmer_type"],
                created_at, normalized["farmer_id"]
            ))
        else:
            con.execute("""
                INSERT INTO farmers (
                    farmer_id, farmer_name, phone_number, preferred_language,
                    intermediary_id, consent_status, consent_language, consent_purpose,
                    consent_timestamp, is_deleted, uploaded_documents,
                    bank_account_name, state, district, crop, land_acres,
                    farmer_type, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                normalized["farmer_id"], normalized["farmer_name"],
                normalized["phone_number"], normalized["preferred_language"],
                normalized["intermediary_id"], normalized["consent_status"],
                normalized["consent_language"], normalized["consent_purpose"],
                normalized["consent_timestamp"], json.dumps(normalized["uploaded_documents"]),
                normalized["bank_account_name"], normalized["state"],
                normalized["district"], normalized["crop"],
                normalized["land_acres"], normalized["farmer_type"],
                created_at,
            ))
        con.commit()

    log_runtime_audit_event(
        action_type="CREATE",
        target_resource="farmer_profile",
        record_id=normalized["farmer_id"],
        actor_id=actor_id or normalized["farmer_id"],
        actor_role="farmer",
        db_path=db_path
    )

    return get_profile(normalized["farmer_id"], db_path=db_path)


def get_profile(farmer_id: str, db_path=None, actor_id: Optional[str] = None, skip_audit: bool = False) -> Optional[Dict[str, Any]]:
    """
    Retrieve farmer profile by unique farmer_id.
    Filters out soft-deleted records.
    """
    init_db(db_path)
    farmer_id_clean = str(farmer_id).strip()
    with connect(db_path) as con:
        row = con.execute(
            "SELECT * FROM farmers WHERE farmer_id = ? AND is_deleted = 0",
            (farmer_id_clean,)
        ).fetchone()

    if not row:
        return None

    if not skip_audit:
        log_runtime_audit_event(
            action_type="READ",
            target_resource="farmer_profile",
            record_id=farmer_id_clean,
            actor_id=actor_id or farmer_id_clean,
            actor_role="farmer",
            db_path=db_path
        )

    return _format_profile_output(row)


def search_farmer(farmer_id: str, db_path=None, actor_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Search farmer by farmer_id. Returns active profile if found, else None.
    """
    return get_profile(farmer_id, db_path=db_path, actor_id=actor_id)


def update_profile(farmer_id: str, updated_data: Dict[str, Any], db_path=None, actor_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Update details for an existing farmer profile.
    Raises ValueError if farmer does not exist or is deleted.
    """
    init_db(db_path)
    _sanitize_and_validate_privacy(updated_data)
    farmer_id_clean = str(farmer_id).strip()

    current_profile = get_profile(farmer_id_clean, db_path=db_path, skip_audit=True)
    if not current_profile:
        raise ValueError(f"Farmer with ID '{farmer_id_clean}' not found.")

    name = updated_data.get("farmer_name") or updated_data.get("name") or current_profile["farmer_name"]
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

    state = updated_data.get("state", current_profile.get("state", "Telangana"))
    district = updated_data.get("district", current_profile.get("district", "Warangal"))
    crop = updated_data.get("crop", current_profile.get("crop", "Paddy"))
    land_acres = float(updated_data.get("land_acres", current_profile.get("land_acres", 2.0)))
    farmer_type = updated_data.get("farmer_type", current_profile.get("farmer_type", "owner"))

    with connect(db_path) as con:
        con.execute("""
            UPDATE farmers SET
                farmer_name = ?, phone_number = ?, preferred_language = ?,
                intermediary_id = ?, consent_status = ?, uploaded_documents = ?,
                bank_account_name = ?, state = ?, district = ?, crop = ?,
                land_acres = ?, farmer_type = ?
            WHERE farmer_id = ? AND is_deleted = 0
        """, (
            str(name).strip(), str(phone).strip(), str(language).strip(),
            str(intermediary_id).strip() if intermediary_id else None,
            consent_int, json.dumps(docs),
            str(bank_name).strip() if bank_name else None,
            str(state).strip(), str(district).strip(), str(crop).strip(),
            land_acres, str(farmer_type).strip(),
            farmer_id_clean,
        ))
        con.commit()

    log_runtime_audit_event(
        action_type="UPDATE",
        target_resource="farmer_profile",
        record_id=farmer_id_clean,
        actor_id=actor_id or farmer_id_clean,
        actor_role="farmer",
        db_path=db_path
    )

    return get_profile(farmer_id_clean, db_path=db_path, skip_audit=True)


def soft_delete_profile(farmer_id: str, db_path=None, actor_id: Optional[str] = None) -> bool:
    """
    Soft-delete and anonymize a farmer's profile upon right-to-be-forgotten request.
    Scrubs PII (name masked, phone cleared, consent revoked) while preserving
    statistical fields for aggregate k-anonymity reports.
    """
    farmer_id_clean = str(farmer_id).strip()
    with connect(db_path) as con:
        masked_name = f"ANONYMIZED_FARMER_{farmer_id_clean[:8]}"
        cur = con.cursor()
        cur.execute("""
            UPDATE farmers SET
                farmer_name = ?,
                phone_number = '',
                consent_status = 0,
                is_deleted = 1,
                bank_account_name = NULL,
                intermediary_id = NULL
            WHERE farmer_id = ? AND is_deleted = 0
        """, (masked_name, farmer_id_clean))
        con.commit()
        if cur.rowcount == 0:
            return False

    log_runtime_audit_event(
        action_type="DELETE",
        target_resource="farmer_profile",
        record_id=farmer_id_clean,
        actor_id=actor_id or farmer_id_clean,
        actor_role="farmer",
        db_path=db_path
    )
    return True


def export_profile_data(farmer_id: str, db_path=None, actor_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Export all data associated with a farmer in portable format.
    """
    profile = get_profile(farmer_id, db_path=db_path, actor_id=actor_id, skip_audit=True)
    if not profile:
        return None

    log_runtime_audit_event(
        action_type="EXPORT",
        target_resource="farmer_profile",
        record_id=farmer_id,
        actor_id=actor_id or farmer_id,
        actor_role="farmer",
        db_path=db_path
    )

    return {
        "export_metadata": {
            "exported_at": datetime.now().isoformat(timespec="seconds"),
            "farmer_id": farmer_id,
            "version": "1.0"
        },
        "profile": profile
    }


def list_all_farmers(db_path=None, active_consent_only=False) -> List[Dict[str, Any]]:
    """
    Internal administrative helper listing active non-deleted farmers.
    """
    init_db(db_path)
    with connect(db_path) as con:
        query = "SELECT * FROM farmers WHERE is_deleted = 0"
        if active_consent_only:
            query += " AND consent_status = 1"
        query += " ORDER BY farmer_name ASC"
        rows = con.execute(query).fetchall()

    return [_format_profile_output(r) for r in rows]
