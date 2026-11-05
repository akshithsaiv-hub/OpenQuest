"""
Feedback Loop & Higher Official Grievance Escalation Engine
1. Feedback Loop: Enables farmers, CSC operators, and field agents to flag outdated or erroneous scheme data.
2. Escalation Mechanism: Generates formal, legally compliant grievance petitions for submission to:
   - Level 1: Agriculture Extension Officer (AEO) at Village Rythu Vedika
   - Level 2: Mandal Agriculture Officer (MAO) / Tahsildar
   - Level 3: District Agriculture Officer (DAO) & District Collector (Prajavani)
   - Level 4: Central Government Public Grievance Portal (CPGRAMS - pgportal.gov.in)
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List

FEEDBACK_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "feedback_store.json")
ESCALATION_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "escalations.json")

def init_stores():
    os.makedirs(os.path.dirname(FEEDBACK_FILE_PATH), exist_ok=True)
    if not os.path.exists(FEEDBACK_FILE_PATH):
        with open(FEEDBACK_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
    if not os.path.exists(ESCALATION_FILE_PATH):
        with open(ESCALATION_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

def record_feedback(
    scheme_id: str,
    scheme_name: str,
    feedback_type: str,
    reporter_role: str,
    description: str,
    state: str = "Telangana"
) -> Dict[str, Any]:
    init_stores()
    try:
        with open(FEEDBACK_FILE_PATH, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)
    except Exception:
        feedbacks = []

    item = {
        "feedback_id": f"FB-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "scheme_id": scheme_id,
        "scheme_name": scheme_name,
        "feedback_type": feedback_type,
        "reporter_role": reporter_role,
        "description": description,
        "state": state,
        "created_at": datetime.now().isoformat(),
        "status": "LOGGED_FOR_CURATION"
    }

    feedbacks.append(item)
    with open(FEEDBACK_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, indent=2)

    return item

def get_all_feedbacks() -> List[Dict[str, Any]]:
    init_stores()
    try:
        with open(FEEDBACK_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def generate_formal_escalation_petition(
    farmer_name: str,
    father_husband_name: str,
    aadhaar_masked: str,
    phone: str,
    village: str,
    mandal: str,
    district: str,
    survey_no: str,
    problem_category: str,
    scheme_name: str,
    description: str,
    escalation_level: str = "Level 2: Mandal Agriculture Officer (MAO)"
) -> Dict[str, Any]:
    """
    Generates a formal representation letter and grievance text addressed to higher authorities.
    """
    init_stores()
    petition_ref = f"GRV/{district.upper()[:3]}/{datetime.now().strftime('%Y%m%d/%H%M')}"
    timestamp_str = datetime.now().strftime("%d-%b-%Y")

    if "Level 1" in escalation_level:
        officer_title = f"The Agriculture Extension Officer (AEO)\nRythu Vedika, {village} / {mandal} Mandal, {district} District"
    elif "Level 2" in escalation_level:
        officer_title = f"The Mandal Agriculture Officer (MAO) & Tahsildar\nOffice of the Mandal Agricultural Officer, {mandal}, {district} District"
    elif "Level 3" in escalation_level:
        officer_title = f"The District Agriculture Officer (DAO) & District Collector\nPrajavani Grievance Cell, Collectorate, {district} District"
    else:
        officer_title = "The Commissioner of Agriculture & Central Public Grievance Portal (CPGRAMS)\nDepartment of Agriculture & Farmers Welfare, Govt of India"

    petition_text = f"""================================================================================
FORMAL GRIEVANCE REPRESENTATION / ప్రజావాణి ఫిర్యాదు దరఖాస్తు
Reference Number: {petition_ref} | Date: {timestamp_str}
================================================================================

To:
{officer_title}

Subject: Urgent Redressal Request regarding {problem_category} under {scheme_name}
         - Regarding Farmer {farmer_name}, Survey No. {survey_no}, Village {village}.

Respected Sir / Madam,

I am {farmer_name}, S/o or W/o {father_husband_name}, a resident and cultivating farmer of {village} Village, {mandal} Mandal, {district} District. 
My farm is situated in Survey / Khata No. {survey_no}.

I respectfully bring the following urgent grievance to your kind notice:

1. SCHEME CONCERNED: {scheme_name}
2. NATURE OF GRIEVANCE: {problem_category}
3. DETAILED STATEMENT OF FACTS:
   {description}

4. IMPACT ON CULTIVATOR:
   Due to the aforesaid issue, I am facing severe financial hardship and delay in statutory entitlements guaranteed under Citizen's Charter and Government Guidelines.

5. PRAYER / SPECIFIC RELIEF SOUGHT:
   I earnestly request your good office to:
   a) Conduct an immediate inquiry / inspection into the delayed or erroneous processing.
   b) Clear the pending approval / disbursement / field loss survey without further delay.
   c) Issue an official acknowledgment and Action Taken Report (ATR) within statutory timelines.

Enclosures Attached:
- Copy of Aadhaar Card ({aadhaar_masked})
- Copy of Land Record / RoR / Pahani for Survey No. {survey_no}
- Bank Passbook front page copy
- Sowing / Cultivation Proof

Yours faithfully,

(Signature / Thumb Impression)
Name: {farmer_name}
Mobile: {phone}
Address: {village} Village, {mandal} Mandal, {district} District
================================================================================
"""

    record = {
        "petition_ref": petition_ref,
        "farmer_name": farmer_name,
        "phone": phone,
        "district": district,
        "problem_category": problem_category,
        "scheme_name": scheme_name,
        "escalation_level": escalation_level,
        "generated_at": datetime.now().isoformat(),
        "petition_text": petition_text
    }

    try:
        with open(ESCALATION_FILE_PATH, "r", encoding="utf-8") as f:
            escs = json.load(f)
    except Exception:
        escs = []

    escs.append(record)
    with open(ESCALATION_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(escs, f, indent=2)

    return record
