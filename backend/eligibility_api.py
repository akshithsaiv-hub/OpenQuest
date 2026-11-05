import json
import os
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from rapidfuzz import fuzz

app = FastAPI(
    title="Farmer Scheme & Eligibility Assistant API",
    description="Deterministic rule-based eligibility engine and intermediary tracking backend.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "schemes_telangana.json")

def load_schemes() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Pydantic Models
class FarmerProfile(BaseModel):
    farmer_id: Optional[str] = "F-TEMP"
    name: Optional[str] = "Farmer"
    state: str = "Telangana"
    district: Optional[str] = "Warangal"
    land_holding_acres: float = Field(default=2.0, ge=0.0)
    crop: str = "Paddy"
    category: str = "marginal"  # marginal (<2.5 acres), small (2.5-5 acres), tenant, medium, large
    is_tenant: bool = False
    has_ccrc: bool = False  # Crop Cultivator Rights Card for tenant
    caste_category: Optional[str] = "BC"  # SC, ST, BC, General
    has_irrigation_well: bool = True
    query: Optional[str] = None
    language: Optional[str] = "en"  # en, te, hi

class SchemeMatchResult(BaseModel):
    scheme_id: str
    name: str
    category: str
    level: str
    eligible: bool
    reasons: List[str]
    benefits_summary: str
    documents_required: List[str]
    deadlines: Dict[str, Any]
    claim_window: Optional[Dict[str, Any]]
    source_url: str
    last_verified: str
    where_to_apply: str

class MatchResponse(BaseModel):
    profile: FarmerProfile
    eligible_schemes: List[SchemeMatchResult]
    ineligible_schemes: List[SchemeMatchResult]
    total_eligible: int
    evaluated_at: str

class AlertRequest(BaseModel):
    farmer_id: str
    channel: str = "telegram"  # telegram, sms, whatsapp
    message: str

# Deterministic Evaluation Engine (Person 1 specification - purely rule-based, no LLM)
def evaluate_farmer(profile: FarmerProfile, scheme: Dict[str, Any]) -> SchemeMatchResult:
    reasons: List[str] = []
    eligible = True
    rules = scheme.get("rules", {})

    # Rule 1: State Check
    allowed_states = rules.get("allowed_states", ["All"])
    if "All" not in allowed_states and profile.state not in allowed_states:
        eligible = False
        reasons.append(f"Scheme is restricted to {', '.join(allowed_states)}; your state is {profile.state}.")
    else:
        reasons.append(f"State '{profile.state}' matches scheme coverage.")

    # Rule 2: Land Holding Boundaries
    min_land = rules.get("min_land_acres")
    max_land = rules.get("max_land_acres")
    if min_land is not None and profile.land_holding_acres < min_land:
        eligible = False
        reasons.append(f"Minimum land required is {min_land} acres (you entered {profile.land_holding_acres} acres).")
    if max_land is not None and profile.land_holding_acres > max_land:
        eligible = False
        reasons.append(f"Maximum land permissible is {max_land} acres (you entered {profile.land_holding_acres} acres).")

    # Rule 3: Tenant & Land Title Rules
    if rules.get("requires_land_title_or_ccrc", False):
        if profile.is_tenant:
            if not profile.has_ccrc and scheme["scheme_id"] == "TS-RB-01":
                # Rythu Bharosa allows tenant only with valid CCRC
                reasons.append("Tenant farmers require Crop Cultivator Rights Card (CCRC) for Rythu Bharosa.")
            elif profile.has_ccrc:
                reasons.append("Tenant eligibility verified via CCRC endorsement.")
        else:
            reasons.append("Landownership title required (Pattadar / Dharani RoR).")

    # Rule 4: Crop Specificity (e.g., PMFBY or MSP)
    allowed_crops = rules.get("allowed_crops")
    if allowed_crops:
        if profile.crop.strip().title() not in [c.title() for c in allowed_crops]:
            eligible = False
            reasons.append(f"Scheme is for crops: {', '.join(allowed_crops)}. Your crop is {profile.crop}.")
        else:
            reasons.append(f"Crop '{profile.crop}' is eligible under this notification.")

    # Rule 5: Infrastructure (Well/Borewell for Micro Irrigation)
    if rules.get("requires_functional_wells_or_borewells", False):
        if not profile.has_irrigation_well:
            eligible = False
            reasons.append("Requires functional borewell/open-well with energisation.")
        else:
            reasons.append("Functional water source available for drip/sprinkler installation.")

    return SchemeMatchResult(
        scheme_id=scheme["scheme_id"],
        name=scheme["name"],
        category=scheme["category"],
        level=scheme["level"],
        eligible=eligible,
        reasons=reasons,
        benefits_summary=scheme["benefits_summary"],
        documents_required=scheme.get("documents_required", []),
        deadlines=scheme.get("deadlines", {}),
        claim_window=scheme.get("claim_window"),
        source_url=scheme["source_url"],
        last_verified=scheme["last_verified"],
        where_to_apply=scheme["where_to_apply"]
    )

@app.get("/")
def read_root():
    return {
        "service": "Farmer Scheme Assistant Engine",
        "pilot_state": "Telangana",
        "status": "online",
        "last_updated": "2026-11-05"
    }

@app.post("/match", response_model=MatchResponse)
def match_schemes(profile: FarmerProfile):
    """Deterministic eligibility matching across all verified schemes."""
    schemes = load_schemes()
    eligible: List[SchemeMatchResult] = []
    ineligible: List[SchemeMatchResult] = []

    for s in schemes:
        result = evaluate_farmer(profile, s)
        if result.eligible:
            eligible.append(result)
        else:
            ineligible.append(result)

    return MatchResponse(
        profile=profile,
        eligible_schemes=eligible,
        ineligible_schemes=ineligible,
        total_eligible=len(eligible),
        evaluated_at=datetime.now().isoformat()
    )

# Sample database of farmers for Intermediary Dashboard (Person 3 interface)
MOCK_FARMERS_DB = [
    {
        "farmer_id": "TS-WAR-001",
        "farmer_name": "Komirelli Ramulu",
        "phone": "+91 98480 12345",
        "state": "Telangana",
        "district": "Warangal",
        "village": "Geesugonda",
        "crop": "Paddy",
        "land_holding_acres": 2.2,
        "category": "Marginal Farmer",
        "scheme_name": "PMFBY Rabi Crop Insurance",
        "doc_status": "pending",
        "pending_documents": ["Sowing Certificate from AEO", "Bank Passbook IFSC update"],
        "aadhaar_name": "Komirelli Ramulu",
        "bank_account_name": "K. Ramulu",
        "name_match_score": 85,
        "name_match_status": "Minor Mismatch (Requires CSC Attestation)",
        "next_deadline": "2026-11-15T23:59:59",
        "days_left": 10,
        "urgent_alert": "PMFBY Rabi enrollment cut-off in 10 days"
    },
    {
        "farmer_id": "TS-NAL-002",
        "farmer_name": "Boda Venkanna",
        "phone": "+91 94401 23456",
        "state": "Telangana",
        "district": "Nalgonda",
        "village": "Miryalaguda",
        "crop": "Cotton",
        "land_holding_acres": 4.5,
        "category": "Small Farmer",
        "scheme_name": "MSP Cotton Procurement 2026",
        "doc_status": "complete",
        "pending_documents": [],
        "aadhaar_name": "Boda Venkanna",
        "bank_account_name": "Boda Venkanna",
        "name_match_score": 100,
        "name_match_status": "Exact Match (NPCI Active)",
        "next_deadline": "2027-01-31T18:00:00",
        "days_left": 87,
        "urgent_alert": "Procurement token available on OPMS portal"
    },
    {
        "farmer_id": "TS-KHM-003",
        "farmer_name": "Banoth Padma",
        "phone": "+91 97012 34567",
        "state": "Telangana",
        "district": "Khammam",
        "village": "Kallur",
        "crop": "Chilli",
        "land_holding_acres": 1.8,
        "category": "Tenant Farmer",
        "scheme_name": "PMFBY Crop Loss Claim (Unseasonal Hail)",
        "doc_status": "pending",
        "pending_documents": ["Crop Damage Photos", "CCRC Agreement copy", "Loss Intimation Form"],
        "aadhaar_name": "Banoth Padma",
        "bank_account_name": "Padma B",
        "name_match_score": 78,
        "name_match_status": "Mismatch Alert! Update Bank Passbook",
        "next_deadline": "2026-11-07T14:00:00",
        "days_left": 2,
        "urgent_alert": "CRITICAL: 72-hour crop loss claim reporting window closes in 48 hours!"
    },
    {
        "farmer_id": "TS-NZB-004",
        "farmer_name": "Mohammad Shabbir",
        "phone": "+91 98660 98765",
        "state": "Telangana",
        "district": "Nizamabad",
        "village": "Armoor",
        "crop": "Maize",
        "land_holding_acres": 3.0,
        "category": "Small Farmer",
        "scheme_name": "TSMIP Drip Irrigation Subsidy",
        "doc_status": "pending",
        "pending_documents": ["Electricity connection bill", "Borewell discharge certificate"],
        "aadhaar_name": "Mohammad Shabbir",
        "bank_account_name": "Mohd Shabbir",
        "name_match_score": 92,
        "name_match_status": "Acceptable Match",
        "next_deadline": "2026-12-31T23:59:59",
        "days_left": 56,
        "urgent_alert": "TSMIP annual subsidy quota verification"
    },
    {
        "farmer_id": "TS-KRM-005",
        "farmer_name": "Gaddam Mallaiah",
        "phone": "+91 99123 45678",
        "state": "Telangana",
        "district": "Karimnagar",
        "village": "Choppadandi",
        "crop": "Paddy",
        "land_holding_acres": 1.5,
        "category": "Marginal Farmer",
        "scheme_name": "Rythu Bharosa Rabi",
        "doc_status": "complete",
        "pending_documents": [],
        "aadhaar_name": "Gaddam Mallaiah",
        "bank_account_name": "Gaddam Mallaiah",
        "name_match_score": 100,
        "name_match_status": "Exact Match",
        "next_deadline": "2026-11-25T23:59:59",
        "days_left": 20,
        "urgent_alert": "Rythu Bharosa verification at Rythu Vedika"
    }
]

@app.get("/farmer_status")
def get_farmer_status(district: Optional[str] = None, doc_status: Optional[str] = None):
    """Intermediary mode API: Fetches farmers with pending documents and approaching deadlines."""
    farmers = MOCK_FARMERS_DB
    if district and district.lower() != "all":
        farmers = [f for f in farmers if f["district"].lower() == district.lower()]
    if doc_status and doc_status.lower() != "all":
        farmers = [f for f in farmers if f["doc_status"].lower() == doc_status.lower()]
    return farmers

@app.post("/verify_name_match")
def verify_name_match(aadhaar_name: str, bank_name: str):
    """Document readiness check: Fuzzy match between Aadhaar name and Bank account name."""
    clean_aadhaar = aadhaar_name.strip().lower().replace(".", " ")
    clean_bank = bank_name.strip().lower().replace(".", " ")
    
    # token_set_ratio handles initial matching and word ordering
    ratio = int(fuzz.token_set_ratio(clean_aadhaar, clean_bank))
    status = "Exact Match" if ratio == 100 else ("Minor Variation" if ratio >= 80 else "Severe Mismatch")
    return {
        "aadhaar_name": aadhaar_name,
        "bank_name": bank_name,
        "similarity_score": ratio,
        "status": status,
        "action_required": "None (Ready for DBT)" if ratio >= 80 else "Visit Bank branch or CSC with Aadhaar to update name."
    }

@app.post("/send_alert")
def send_proactive_alert(req: AlertRequest):
    """Sends / simulates proactive deadline alert to the farmer."""
    farmer = next((f for f in MOCK_FARMERS_DB if f["farmer_id"] == req.farmer_id), None)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    return {
        "status": "success",
        "farmer_id": req.farmer_id,
        "farmer_name": farmer["farmer_name"],
        "channel": req.channel,
        "sent_to": farmer["phone"],
        "message": req.message,
        "timestamp": datetime.now().isoformat()
    }

# Live MSP vs Mandi Benchmark endpoint
@app.get("/msp_comparison")
def get_msp_comparison():
    return [
        {
            "crop": "Paddy (Common / Grade A)",
            "msp_rate": 2320,
            "state_bonus": 500,
            "effective_gov_price": 2820,
            "average_mandi_price": 2180,
            "price_delta": 640,
            "recommendation": "Sell at government PACS / IKP procurement centre to gain +₹640/quintal over open market.",
            "source": "Telangana Civil Supplies Corporation (epds.telangana.gov.in)"
        },
        {
            "crop": "Cotton (Medium Staple)",
            "msp_rate": 7121,
            "state_bonus": 0,
            "effective_gov_price": 7121,
            "average_mandi_price": 6850,
            "price_delta": 271,
            "recommendation": "Sell to Cotton Corporation of India (CCI) procurement centre at MSP of ₹7,121.",
            "source": "Cotton Corporation of India (CCI)"
        },
        {
            "crop": "Maize",
            "msp_rate": 2225,
            "state_bonus": 0,
            "effective_gov_price": 2225,
            "average_mandi_price": 2100,
            "price_delta": 125,
            "recommendation": "MSP procurement offers ₹125/quintal premium over local trader bids.",
            "source": "Commission for Agricultural Costs and Prices (CACP)"
        }
    ]

# Live Climate & Water Stress Assessment endpoint
@app.get("/climate_water_stress")
def get_climate_water_stress(district: str = "Warangal", crop: str = "Paddy", water_source: str = "Borewell", lang: str = "en"):
    from utils.weather_api import get_live_weather, evaluate_water_stress, generate_multilingual_water_advisory
    weather = get_live_weather(district)
    assessment = evaluate_water_stress(weather, crop=crop, water_source=water_source)
    advisory_text = generate_multilingual_water_advisory(assessment, lang=lang)
    return {
        "weather": weather,
        "assessment": assessment,
        "advisory_text": advisory_text
    }
