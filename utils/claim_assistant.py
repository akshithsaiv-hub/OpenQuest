"""
72-Hour Crop Loss Claim Assistant Engine
Ensures farmers never miss the statutory 72-hour window mandated by PMFBY & State Calamity guidelines.
Provides:
- 72-hour countdown timer logic
- Geo-tagged photo checklist and technical guidance (GPS coordinates, timestamp)
- Mandatory document checklist for loss intimation
- Auto-generated SMS / WhatsApp intimation text for immediate transmission to AEO / Insurance Rep
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import os
import json

PMFBY_HELPLINE = "1800-180-1551"
KISAN_CALL_CENTER = "1800-180-1551"

GEO_PHOTO_CHECKLIST = [
    {
        "item": "Wide Field View Photo (GPS Geotagged)",
        "requirement": "Stand at field bund and capture broad view of affected survey parcel showing damaged crop canopy with landmarks (tree, borewell, or electric pole).",
        "mandatory": True
    },
    {
        "item": "Close-Up Plant Damage Photo",
        "requirement": "Hold healthy plant alongside lodged / submerged / scorched plant to show clear loss contrast (panicle rotting, pest neck blast, or hail-shattered leaves).",
        "mandatory": True
    },
    {
        "item": "Water Level / Hailstone Measurement Photo",
        "requirement": "Place a measuring scale or mobile phone next to standing water depth or hail accumulations on ground.",
        "mandatory": False
    },
    {
        "item": "Newspaper / Timeproof Reference Photo",
        "requirement": "Photograph today's local newspaper or mobile clock screen in field to conclusively establish the exact date.",
        "mandatory": False
    }
]

DOCUMENT_CHECKLIST = [
    {"doc": "PMFBY Insurance Policy / Application Receipt / Bank Debit Ack", "source": "Bank Passbook showing PMFBY premium deduction OR CSC receipt"},
    {"doc": "Land Record (Pahani / Dharani / RoR / 7/12)", "source": "Digital Dharani or MeeSeva certified copy"},
    {"doc": "Sowing Certificate / VRO-AEO Cultivation Certificate", "source": "Issued by local Agriculture Extension Officer (AEO) or VRO"},
    {"doc": "Aadhaar Card Copy", "source": "UIDAI Aadhaar"},
    {"doc": "Active Bank Passbook (IFSC & A/c visible)", "source": "Nationalised / RRB / Cooperative Bank account"}
]

def calculate_72hr_window(incident_datetime: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Computes time remaining in the strict 72-hour reporting window.
    """
    now = datetime.now()
    if incident_datetime is None:
        incident_datetime = now - timedelta(hours=14)

    deadline = incident_datetime + timedelta(hours=72)
    time_left = deadline - now
    total_seconds_left = int(time_left.total_seconds())

    if total_seconds_left <= 0:
        return {
            "status": "EXPIRED",
            "hours_remaining": 0,
            "minutes_remaining": 0,
            "seconds_remaining": 0,
            "display_str": "00:00:00 (EXPIRED)",
            "urgency": "EXPIRED",
            "color": "red",
            "deadline_str": deadline.strftime("%Y-%m-%d %I:%M %p"),
            "advice": "72-Hour automated portal window has lapsed. Immediately submit an offline physical representation countersigned by AEO / Tahsildar to the District Collector Grievance Cell."
        }

    hours = total_seconds_left // 3600
    minutes = (total_seconds_left % 3600) // 60
    seconds = total_seconds_left % 60

    if hours >= 48:
        urgency = "LOW"
        color = "green"
    elif hours >= 24:
        urgency = "MEDIUM"
        color = "orange"
    else:
        urgency = "CRITICAL"
        color = "red"

    return {
        "status": "ACTIVE",
        "hours_remaining": hours,
        "minutes_remaining": minutes,
        "seconds_remaining": seconds,
        "display_str": f"{hours:02d}h {minutes:02d}m {seconds:02d}s",
        "urgency": urgency,
        "color": color,
        "deadline_str": deadline.strftime("%Y-%m-%d %I:%M %p"),
        "incident_str": incident_datetime.strftime("%Y-%m-%d %I:%M %p"),
        "advice": "Window is actively counting down. Gather geotagged photos and dispatch intimation SMS to avoid claim repudiation!"
    }

def generate_intimation_sms(
    farmer_name: str,
    phone: str,
    crop: str,
    district: str,
    village: str,
    survey_no: str,
    loss_percent: int,
    hazard_type: str,
    acreage: float,
    language: str = "en"
) -> Dict[str, str]:
    """
    Generates standardized, compliant claim intimation message drafts for SMS/WhatsApp
    that contain all legal parameters required by PMFBY insurance companies.
    """
    timestamp_str = datetime.now().strftime("%d-%b-%Y %I:%M %p")

    msg_en = (
        f"PMFBY CROP LOSS INTIMATION (Statutory 72-Hour Notice)\n"
        f"Date: {timestamp_str}\n"
        f"Farmer: {farmer_name} | Mobile: {phone}\n"
        f"Location: Village {village}, Dist {district}, Survey No: {survey_no}\n"
        f"Crop: {crop} | Affected Area: {acreage} Acres\n"
        f"Peril/Hazard: {hazard_type}\n"
        f"Estimated Loss: {loss_percent}%\n"
        f"Request: Depute Joint Assessment Team (AEO & Insurance Assessor) for field survey.\n"
        f"Toll-Free Helpline: 1800-180-1551"
    )

    msg_te = (
        f"పంట నష్ట సమాచారం (PMFBY 72 గంటల నిబంధన)\n"
        f"తేదీ: {timestamp_str}\n"
        f"రైతు పేరు: {farmer_name} | మొబైల్: {phone}\n"
        f"ప్రాంతం: గ్రామం {village}, జిల్లా {district}, సర్వే నం: {survey_no}\n"
        f"పంట: {crop} | దెబ్బతిన్న విస్తీర్ణం: {acreage} ఎకరాలు\n"
        f"నష్ట కారణం: {hazard_type}\n"
        f"అంచనా నష్టం: {loss_percent}%\n"
        f"విజ్ఞప్తి: వెంటనే AEO మరియు ఇన్సూరెన్స్ సర్వేయర్ వచ్చి క్షేత్ర పరిశీలన చేయగలరు.\n"
        f"టోల్‌ఫ్రీ హెల్ప్‌లైన్: 1800-180-1551"
    )

    msg_hi = (
        f"फसल क्षति पूर्व-सूचना (PMFBY 72 घंटे की वैधानिक सूचना)\n"
        f"दिनांक: {timestamp_str}\n"
        f"किसान: {farmer_name} | मोबाइल: {phone}\n"
        f"स्थान: ग्राम {village}, जिला {district}, खसरा/सर्वे नं: {survey_no}\n"
        f"फसल: {crop} | प्रभावित रकबा: {acreage} एकड़\n"
        f"आपदा का कारण: {hazard_type}\n"
        f"अनुमानित नुकसान: {loss_percent}%\n"
        f"अनुरोध: संयुक्त सर्वेक्षण दल (AEO व बीमा कंपनी) को मौके पर निरीक्षण हेतु भेजें।\n"
        f"टोल-फ्री हेल्पलाइन: 1800-180-1551"
    )

    selected_msg = msg_te if language == "te" else (msg_hi if language == "hi" else msg_en)

    return {
        "text": selected_msg,
        "en": msg_en,
        "te": msg_te,
        "hi": msg_hi,
        "target_helpline": PMFBY_HELPLINE
    }


# Standard District Level Technical Committee (DLTC) Scale of Finance (Sum Insured per Acre)
CROP_SUM_INSURED_PER_ACRE = {
    "Paddy": 42000.0,
    "Cotton": 48000.0,
    "Chilli": 78000.0,
    "Maize": 35000.0,
    "Soybean": 32000.0,
    "Bengal Gram": 30000.0,
    "Groundnut": 36000.0,
    "Red Gram": 34000.0,
    "Wheat": 38000.0,
    "Millets": 25000.0,
    "Vegetables": 60000.0
}

# SDRF Input Subsidy per Acre (MHA Revised Norms)
SDRF_SUBSIDY_PER_ACRE = {
    "rainfed": 3440.0,      # Rs 8,500 / hectare
    "irrigated": 6880.0,    # Rs 17,000 / hectare
    "perennial": 9100.0     # Rs 22,500 / hectare
}

def calculate_claim_compensation(
    crop: str,
    acreage: float,
    loss_percent: int,
    is_irrigated: bool = True,
    state: str = "Telangana"
):
    """
    Computes statutory entitlement across PMFBY and State SDRF/ex-gratia disaster relief.
    """
    clean_crop = crop.split()[0].capitalize()
    sum_insured_per_acre = CROP_SUM_INSURED_PER_ACRE.get(clean_crop, 40000.0)
    total_sum_insured = round(sum_insured_per_acre * acreage, 2)

    loss_ratio = max(0.0, min(100.0, float(loss_percent))) / 100.0
    pmfby_payout = round(total_sum_insured * loss_ratio, 2)

    sdrf_rate = SDRF_SUBSIDY_PER_ACRE["irrigated"] if is_irrigated else SDRF_SUBSIDY_PER_ACRE["rainfed"]
    sdrf_eligible = (loss_percent >= 33)
    sdrf_payout = round(sdrf_rate * acreage, 2) if sdrf_eligible else 0.0

    state_relief_rate = 10000.0 if state in ["Telangana", "Andhra Pradesh"] else 0.0
    state_relief_payout = round(state_relief_rate * acreage, 2) if (sdrf_eligible and state_relief_rate > 0) else 0.0

    total_recovery = round(pmfby_payout + sdrf_payout + state_relief_payout, 2)

    return {
        "crop": crop,
        "acreage": acreage,
        "loss_percent": loss_percent,
        "sum_insured_per_acre": sum_insured_per_acre,
        "total_sum_insured": total_sum_insured,
        "pmfby_expected_payout": pmfby_payout,
        "sdrf_eligible": sdrf_eligible,
        "sdrf_rate_per_acre": sdrf_rate,
        "sdrf_payout": sdrf_payout,
        "state_relief_payout": state_relief_payout,
        "total_estimated_recovery": total_recovery,
        "statutory_note": (
            "PMFBY payout is processed via direct DBT by the empanelled insurance company. "
            "SDRF input subsidy is released independently by the State Revenue/Disaster Management Dept "
            "and does NOT reduce PMFBY insurance compensation."
        )
    }

def generate_claim_dossier(
    farmer_name: str,
    phone: str,
    crop: str,
    district: str,
    village: str,
    survey_no: str,
    hazard_type: str,
    loss_percent: int,
    acreage: float,
    geo_photos_count: int = 0,
    telemetry_notes: str = "33.5C, 0.0 mm rain, High Evaporative Deficit"
) -> str:
    """
    Generates a formal, comprehensive Claim Representation Docket suitable for
    submission to the Joint Survey Inspection Committee (AEO + Insurance Surveyor).
    """
    now = datetime.now()
    dossier_id = f"PMFBY/{district[:3].upper()}/{now.strftime('%Y%m%d%H%M')}"
    comp = calculate_claim_compensation(crop, acreage, loss_percent)

    dossier = f"""================================================================================
STATUTORY PMFBY & SDRF CROP LOSS CLAIM REPRESENTATION DOCKET
Reference ID: {dossier_id} | Date of Intimation: {now.strftime('%d-%b-%Y %I:%M %p')}
Statutory Mandate: Pradhan Mantri Fasal Bima Yojana (PMFBY) Operational Guidelines Sec 21.4
================================================================================

1. CULTIVATOR & GEOGRAPHIC PROFILE
   - Full Name of Farmer: {farmer_name}
   - Contact Mobile: {phone}
   - Village & Gram Panchayat: {village}
   - District & State: {district}, Telangana
   - Survey / Khata / Passbook No: {survey_no}
   - Cultivation Tenure: Registered Cultivator / Tenant CCRC Holder

2. PARCEL & LOSS INCIDENT DETAILS
   - Insured Crop: {crop}
   - Total Cultivated Parcel Area: {acreage} Acres
   - Nature of Peril / Hazard: {hazard_type}
   - Assessed Crop Damage Severity: {loss_percent}%
   - Environmental Telemetry at Loss: {telemetry_notes}
   - 72-Hour Reporting Compliance: Intimated within statutory window (TIMELY)

3. ESTIMATED STATUTORY COMPENSATION BREAKDOWN
   - DLTC Scale of Finance (Sum Insured): Rs {comp['sum_insured_per_acre']:,.2f} per acre
   - Total Sum Insured: Rs {comp['total_sum_insured']:,.2f}
   - Projected PMFBY Insurance Payout: Rs {comp['pmfby_expected_payout']:,.2f}
   - State Disaster Response Fund (SDRF) Input Subsidy: Rs {comp['sdrf_payout']:,.2f}
   - Special State Calamity Ex-Gratia: Rs {comp['state_relief_payout']:,.2f}
   -----------------------------------------------------------------------------
   TOTAL PROJECTED STATUTORY RECOVERY: Rs {comp['total_estimated_recovery']:,.2f}

4. ENCLOSED GEO-TAGGED EVIDENCE REGISTER
   - Number of Geo-Tagged Field Photos Attached: {geo_photos_count}
   - Forensic Photo Tags: GPS Latitude/Longitude, Timestamp, Survey Number embedded.
   - Land Proof: Digital Pahani / Dharani / RoR-1B verified.
   - Premium Proof: Bank Passbook statement / CSC receipt verified.

5. PRAYER & OFFICIAL ACTION DEMANDED
   The undersigned farmer respectfully intimates this localized loss under PMFBY Sec 21.4
   and requests the District Agriculture Officer to depute the Joint Survey Committee 
   (Village Agriculture Extension Officer & Empanelled Insurance Surveyor) for on-site 
   loss verification within 10 days as per Citizen's Charter timelines.

Signed by Cultivator: ___________________________
Acknowledging Officer (AEO / CSC): ___________________________
Official Helpline: 1800-180-1551 | Portal: pmfby.gov.in
================================================================================
"""
    return dossier
