"""
Farmer Document Wallet & Consent-Driven Digital Locker Integration
Supports strictly storing, viewing, replacing, and reviewing the Farmer Bank Passbook / DBT Mandate.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional

VAULT_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "document_vault.json")

SUPPORTED_DOC_TYPES = [
    {
        "id": "bank_passbook",
        "name": "Farmer Bank Passbook / DBT Mandate",
        "essential_for": ["Direct Benefit Transfer (DBT)", "PMFBY Claim Settlement", "Rythu Bharosa Subsidies", "KCC Loan Processing"]
    }
]

def init_vault():
    os.makedirs(os.path.dirname(VAULT_DATA_PATH), exist_ok=True)
    if not os.path.exists(VAULT_DATA_PATH):
        with open(VAULT_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "vault_version": "2.0",
                "last_updated": datetime.now().isoformat(),
                "farmers": {
                    "DEMO_FARMER_1": {
                        "farmer_id": "DEMO_FARMER_1",
                        "farmer_name": "Komirelli Ramulu",
                        "agristack_farmer_id": "AGRI-IN-TS-WAR-88392",
                        "digilocker_linked": True,
                        "consent_granted": True,
                        "consent_timestamp": "2026-11-01T10:00:00",
                        "documents": [
                            {
                                "doc_type": "bank_passbook",
                                "title": "Telangana Grameena Bank Passbook",
                                "identifier_masked": "A/C: *******8821 (IFSC: SBIN0RRTSGB)",
                                "verified": True,
                                "source": "Physical Scan Uploaded",
                                "uploaded_at": "2026-11-01T10:10:00",
                                "uri": "local://vault/bank_passbook_ramulu.pdf"
                            }
                        ]
                    }
                }
            }, f, indent=2)

def get_farmer_documents(farmer_id: str = "DEMO_FARMER_1") -> Dict[str, Any]:
    init_vault()
    try:
        with open(VAULT_DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        farmer_entry = data.get("farmers", {}).get(farmer_id, {
            "farmer_id": farmer_id,
            "consent_granted": False,
            "documents": []
        })
        # Filter strictly to bank_passbook
        docs = [d for d in farmer_entry.get("documents", []) if d.get("doc_type") == "bank_passbook"]
        farmer_entry["documents"] = docs
        return farmer_entry
    except Exception:
        return {"farmer_id": farmer_id, "consent_granted": False, "documents": []}

def add_farmer_document(
    farmer_id: str,
    farmer_name: str,
    doc_type: str,
    title: str,
    identifier: str,
    source: str = "Manual Scan Upload",
    consent: bool = True
) -> Dict[str, Any]:
    if doc_type != "bank_passbook":
        raise ValueError(f"Document type '{doc_type}' is not supported. The Document Wallet strictly supports only 'bank_passbook'.")

    init_vault()
    with open(VAULT_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if farmer_id not in data["farmers"]:
        data["farmers"][farmer_id] = {
            "farmer_id": farmer_id,
            "farmer_name": farmer_name,
            "agristack_farmer_id": f"AGRI-IN-TS-{hashlib.md5(farmer_id.encode()).hexdigest()[:6].upper()}",
            "digilocker_linked": "digilocker" in source.lower(),
            "consent_granted": consent,
            "consent_timestamp": datetime.now().isoformat(),
            "documents": []
        }

    masked = identifier[-4:].rjust(len(identifier), "X") if len(identifier) > 4 else identifier

    new_doc = {
        "doc_type": "bank_passbook",
        "title": title or "Farmer Bank Passbook / DBT Mandate",
        "identifier_masked": masked,
        "verified": True if "digilocker" in source.lower() else False,
        "source": source,
        "uploaded_at": datetime.now().isoformat(),
        "uri": f"vault://{farmer_id}/passbook_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }

    docs = data["farmers"][farmer_id]["documents"]
    docs = [d for d in docs if d["doc_type"] != "bank_passbook"]
    docs.append(new_doc)
    data["farmers"][farmer_id]["documents"] = docs
    data["farmers"][farmer_id]["consent_granted"] = consent
    data["last_updated"] = datetime.now().isoformat()

    with open(VAULT_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return new_doc

def check_scheme_document_readiness(required_docs: List[str], farmer_id: str = "DEMO_FARMER_1") -> Dict[str, Any]:
    """
    Evaluates whether the farmer has uploaded the mandatory bank passbook for DBT / scheme readiness.
    """
    farmer_data = get_farmer_documents(farmer_id)
    uploaded_types = {d["doc_type"] for d in farmer_data.get("documents", [])}

    has_passbook = "bank_passbook" in uploaded_types

    matching = []
    missing = []

    for req in required_docs:
        req_clean = req.lower()
        if any(w in req_clean for w in ["bank", "passbook", "ifsc", "account"]):
            if has_passbook:
                matching.append(req)
            else:
                missing.append(req)
        else:
            # Other document requirements are verified via official state records (Aadhaar e-KYC, Dharani, CCRC)
            matching.append(req)

    pct = round((len(matching) / len(required_docs) * 100), 1) if required_docs else 100.0

    return {
        "is_ready": len(missing) == 0,
        "readiness_percent": pct,
        "matching_docs": matching,
        "missing_docs": missing,
        "digilocker_linked": farmer_data.get("digilocker_linked", False)
    }
