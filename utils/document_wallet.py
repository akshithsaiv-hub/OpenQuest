"""
Farmer Document Wallet & Consent-Driven Digital Locker Integration
Supports storing scanned land records, IDs, CCRC certificates, and bank passbooks with farmer consent.
Provides compatibility with AgriStack Farmer ID & DigiLocker URI schemes.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional

VAULT_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "document_vault.json")

SUPPORTED_DOC_TYPES = [
    {"id": "aadhaar", "name": "Aadhaar Card (UIDAI)", "essential_for": ["PM-KISAN", "Rythu Bharosa", "PMFBY", "KCC"]},
    {"id": "land_record", "name": "Land Record (Pahani / Dharani / 7/12 / RoR 1B)", "essential_for": ["Rythu Bharosa", "PMKSY", "KCC", "MSP"]},
    {"id": "bank_passbook", "name": "Bank Passbook with active IFSC & A/c", "essential_for": ["DBT Subsidies", "Disaster Relief", "PMFBY"]},
    {"id": "ccrc_tenancy", "name": "CCRC Card / Registered Tenancy Agreement", "essential_for": ["Tenant Farmer Rythu Bharosa", "Crop Insurance"]},
    {"id": "sowing_cert", "name": "Sowing / Cultivation Certificate (AEO issued)", "essential_for": ["PMFBY Loss Claim", "Disaster Relief Input Subsidy"]},
    {"id": "caste_cert", "name": "Social Category / Caste Certificate (MeeSeva)", "essential_for": ["TSMIP 100% Subsidy", "Special SC/ST grants"]},
    {"id": "soil_health", "name": "Soil Health Card (SHC)", "essential_for": ["Subsidised Micro-Nutrients", "Soil Reconditioning"]}
]

def init_vault():
    os.makedirs(os.path.dirname(VAULT_DATA_PATH), exist_ok=True)
    if not os.path.exists(VAULT_DATA_PATH):
        with open(VAULT_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "vault_version": "1.0",
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
                                "doc_type": "aadhaar",
                                "title": "Aadhaar Card",
                                "identifier_masked": "XXXX-XXXX-4921",
                                "verified": True,
                                "source": "DigiLocker Verified",
                                "uploaded_at": "2026-11-01T10:05:00",
                                "uri": "digilocker://in.gov.uidai/aadhaar/4921"
                            },
                            {
                                "doc_type": "land_record",
                                "title": "Dharani RoR Passbook (Survey 142/A)",
                                "identifier_masked": "T192004210",
                                "verified": True,
                                "source": "Dharani Portal API Sync",
                                "uploaded_at": "2026-11-01T10:06:00",
                                "uri": "dharani://telangana.gov.in/passbook/T192004210"
                            },
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
        return data.get("farmers", {}).get(farmer_id, {
            "farmer_id": farmer_id,
            "consent_granted": False,
            "documents": []
        })
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
        "doc_type": doc_type,
        "title": title,
        "identifier_masked": masked,
        "verified": True if "digilocker" in source.lower() else False,
        "source": source,
        "uploaded_at": datetime.now().isoformat(),
        "uri": f"vault://{farmer_id}/{doc_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }

    docs = data["farmers"][farmer_id]["documents"]
    docs = [d for d in docs if d["doc_type"] != doc_type]
    docs.append(new_doc)
    data["farmers"][farmer_id]["documents"] = docs
    data["farmers"][farmer_id]["consent_granted"] = consent
    data["last_updated"] = datetime.now().isoformat()

    with open(VAULT_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return new_doc

def check_scheme_document_readiness(required_docs: List[str], farmer_id: str = "DEMO_FARMER_1") -> Dict[str, Any]:
    """
    Evaluates whether the farmer has uploaded all mandatory documents required for a specific scheme.
    """
    farmer_data = get_farmer_documents(farmer_id)
    uploaded_types = {d["doc_type"] for d in farmer_data.get("documents", [])}

    matching = []
    missing = []

    for req in required_docs:
        req_clean = req.lower()
        matched = False
        if any(w in req_clean for w in ["aadhaar", "uid"]):
            matched = "aadhaar" in uploaded_types
        elif any(w in req_clean for w in ["land", "pahani", "dharani", "ror", "7/12", "patta", "passbook"]):
            matched = "land_record" in uploaded_types
        elif any(w in req_clean for w in ["bank", "ifsc", "account"]):
            matched = "bank_passbook" in uploaded_types
        elif any(w in req_clean for w in ["ccrc", "tenant"]):
            matched = "ccrc_tenancy" in uploaded_types
        elif any(w in req_clean for w in ["caste", "category"]):
            matched = "caste_cert" in uploaded_types
        elif any(w in req_clean for w in ["sowing", "cultivation"]):
            matched = "sowing_cert" in uploaded_types

        if matched:
            matching.append(req)
        else:
            missing.append(req)

    pct = round((len(matching) / len(required_docs) * 100), 1) if required_docs else 100.0

    return {
        "is_ready": len(missing) == 0,
        "readiness_percent": pct,
        "matching_docs": matching,
        "missing_docs": missing,
        "digilocker_linked": farmer_data.get("digilocker_linked", False)
    }
