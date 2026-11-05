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
