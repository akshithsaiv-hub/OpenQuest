"""
Farmer Claim and Application Status Tracker
Allows farmers and CSC intermediaries to manually log, update, and track status for schemes
where public APIs are restricted or offline.
Generates automated reminder schedules and follow-up alerts when application review exceeds SLA.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

CLAIMS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "farmer_claims.json")

DEFAULT_CLAIMS_DATA = [
    {
        "claim_id": "CLM-2026-TS-001",
        "farmer_id": "F-DEMO-01",
        "farmer_name": "Komirelli Ramulu",
        "phone": "9848022338",
        "scheme_name": "PMFBY Hailstorm Crop Loss Claim",
        "reference_number": "PMFBY/TS/2026/092144",
        "filing_date": (datetime.now() - timedelta(days=18)).strftime("%Y-%m-%d"),
        "status": "Joint Field Survey Completed",
        "status_code": "UNDER_VERIFICATION",
        "handling_officer": "AEO K. Srinivas (Rythu Vedika Geesugonda)",
        "expected_sla_days": 15,
        "notes": "Joint survey photos uploaded. Compensation calculation pending approval at DAO office.",
        "reminders": [
            {"date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"), "type": "SLA_BREACH", "msg": "15-day PMFBY joint survey assessment window crossed. Follow up with Insurance Assessor."}
        ]
    },
    {
        "claim_id": "CLM-2026-TS-002",
        "farmer_id": "F-DEMO-02",
        "farmer_name": "B. Lakshmi",
        "phone": "9440188219",
        "scheme_name": "TSMIP Micro-Irrigation Drip Subsidy",
        "reference_number": "TSMIP/NAL/2026/5521",
        "filing_date": (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d"),
        "status": "Administrative Sanction Approved",
        "status_code": "SANCTIONED",
        "handling_officer": "Horticulture Officer Nalgonda",
        "expected_sla_days": 21,
        "notes": "Farmer 10% DD paid. Company allotment for drip pipeline installation pending.",
        "reminders": [
            {"date": (datetime.now() + timedelta(days=13)).strftime("%Y-%m-%d"), "type": "UPCOMING", "msg": "Installation scheduled within next 13 days."}
        ]
    }
]

def init_claims_store():
    os.makedirs(os.path.dirname(CLAIMS_FILE_PATH), exist_ok=True)
    if not os.path.exists(CLAIMS_FILE_PATH):
        with open(CLAIMS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CLAIMS_DATA, f, indent=2)

def get_all_claims() -> List[Dict[str, Any]]:
    init_claims_store()
    try:
        with open(CLAIMS_FILE_PATH, "r", encoding="utf-8") as f:
            raw_claims = json.load(f)
            # Deduplicate by reference number, keeping the latest entry
            seen_refs = set()
            deduped = []
            for c in reversed(raw_claims):
                ref = c.get("reference_number", "")
                if ref and ref in seen_refs:
                    continue
                if ref:
                    seen_refs.add(ref)
                deduped.append(c)
            return list(reversed(deduped))
    except Exception:
        return DEFAULT_CLAIMS_DATA

def add_claim_entry(
    farmer_name: str,
    phone: str,
    scheme_name: str,
    reference_number: str,
    status: str,
    notes: str = "",
    filing_date_str: str = ""
) -> Dict[str, Any]:
    claims = get_all_claims()
    filing_date = filing_date_str if filing_date_str else datetime.now().strftime("%Y-%m-%d")
    claim_id = f"CLM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    new_claim = {
        "claim_id": claim_id,
        "farmer_id": f"F-{phone[-4:]}",
        "farmer_name": farmer_name,
        "phone": phone,
        "scheme_name": scheme_name,
        "reference_number": reference_number,
        "filing_date": filing_date,
        "status": status,
        "status_code": "ACTIVE",
        "handling_officer": "Local Agriculture Office / CSC",
        "expected_sla_days": 15,
        "notes": notes,
        "reminders": [
            {
                "date": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
                "type": "FOLLOWUP_SCHEDULED",
                "msg": f"Follow-up reminder for {scheme_name} (Ref: {reference_number})"
            }
        ]
    }

    claims.append(new_claim)
    with open(CLAIMS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(claims, f, indent=2)

    return new_claim

def compute_claim_urgency(claim: Dict[str, Any]) -> Dict[str, Any]:
    try:
        filing_dt = datetime.strptime(claim["filing_date"], "%Y-%m-%d")
        days_elapsed = (datetime.now() - filing_dt).days
    except Exception:
        days_elapsed = 5

    sla = claim.get("expected_sla_days", 15)
    is_overdue = days_elapsed > sla and claim.get("status_code") not in ["DISBURSED", "SANCTIONED"]

    if is_overdue:
        urgency = "HIGH"
        status_banner = f"⚠️ Overdue by {days_elapsed - sla} days! Escalate to District Officer / CPGRAMS."
        color = "red"
    elif days_elapsed > (sla - 4):
        urgency = "MEDIUM"
        status_banner = f"⏳ Approaching SLA ({days_elapsed}/{sla} days elapsed)."
        color = "orange"
    else:
        urgency = "NORMAL"
        status_banner = f"✅ In Progress ({days_elapsed}/{sla} days elapsed)."
        color = "green"

    return {
        "days_elapsed": days_elapsed,
        "sla_days": sla,
        "is_overdue": is_overdue,
        "urgency": urgency,
        "status_banner": status_banner,
        "color": color
    }

def delete_claim_entry(ref_or_id: str) -> bool:
    """
    Removes a claim or application entry by reference number or claim_id.
    """
    init_claims_store()
    try:
        with open(CLAIMS_FILE_PATH, "r", encoding="utf-8") as f:
            claims = json.load(f)
        
        filtered = [c for c in claims if c.get("reference_number") != ref_or_id and c.get("claim_id") != ref_or_id]
        if len(filtered) < len(claims):
            with open(CLAIMS_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(filtered, f, indent=2)
            return True
        return False
    except Exception:
        return False
