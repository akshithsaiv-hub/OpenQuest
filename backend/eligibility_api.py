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
    description="Deterministic rule-based eligibility engine, 72-hr claim assistant, water subsidies, KCC credit, and intermediary tracking backend.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, "data", "schemes_telangana.json")
WATER_SCHEMES_PATH = os.path.join(ROOT_DIR, "data", "water_saving_schemes.json")
LOW_WATER_CROPS_PATH = os.path.join(ROOT_DIR, "data", "low_water_crops.json")
DISASTER_RELIEF_PATH = os.path.join(ROOT_DIR, "data", "disaster_relief.json")

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
    category: str = "marginal"
    is_tenant: bool = False
    has_ccrc: bool = False
    caste_category: Optional[str] = "BC"
    has_irrigation_well: bool = True
    query: Optional[str] = None
    language: Optional[str] = "en"

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
    channel: str = "telegram"
    message: str

class KCCRequest(BaseModel):
    crop: str = "Paddy"
    land_acres: float = 2.5
    existing_debt: float = 0.0

class ClaimIntimationRequest(BaseModel):
    farmer_name: str
    phone: str
    crop: str
    district: str
    village: str
    survey_no: str
    loss_percent: int
    hazard_type: str
    acreage: float
    language: str = "en"

class ClaimEntryRequest(BaseModel):
    farmer_name: str
    phone: str
    scheme_name: str
    reference_number: str
    status: str
    notes: Optional[str] = ""

class FeedbackRequest(BaseModel):
    scheme_id: str
    scheme_name: str
    feedback_type: str
    reporter_role: str
    description: str
    state: str = "Telangana"

class EscalationRequest(BaseModel):
    farmer_name: str
    father_husband_name: str
    aadhaar_masked: str
    phone: str
    village: str
    mandal: str
    district: str
    survey_no: str
    problem_category: str
    scheme_name: str
    description: str
    escalation_level: str = "Level 2: Mandal Agriculture Officer (MAO)"

# Deterministic Evaluation Engine
def evaluate_farmer(profile: FarmerProfile, scheme: Dict[str, Any]) -> SchemeMatchResult:
    reasons: List[str] = []
    eligible = True
    rules = scheme.get("rules", {})

    allowed_states = rules.get("allowed_states", ["All"])
    if "All" not in allowed_states and profile.state not in allowed_states:
        eligible = False
        reasons.append(f"Scheme is restricted to {', '.join(allowed_states)}; your state is {profile.state}.")
    else:
        reasons.append(f"State '{profile.state}' matches scheme coverage.")

    min_land = rules.get("min_land_acres")
    max_land = rules.get("max_land_acres")
    if min_land is not None and profile.land_holding_acres < min_land:
        eligible = False
        reasons.append(f"Minimum land required is {min_land} acres (you entered {profile.land_holding_acres} acres).")
    if max_land is not None and profile.land_holding_acres > max_land:
        eligible = False
        reasons.append(f"Maximum land permissible is {max_land} acres (you entered {profile.land_holding_acres} acres).")

    if rules.get("requires_land_title_or_ccrc", False):
        if profile.is_tenant:
            if not profile.has_ccrc:
                eligible = False
                reasons.append("Tenant farmers must possess an active CCRC (Crop Cultivator Rights Card).")
            else:
                reasons.append("CCRC certificate validated for tenant cultivator.")
        else:
            reasons.append("Landownership title record (Pahani / Dharani / RoR) eligible.")

    notified_crops = rules.get("notified_crops", ["All"])
    if "All" not in notified_crops and profile.crop not in notified_crops:
        eligible = False
        reasons.append(f"Crop '{profile.crop}' is not in notified list for this scheme season ({', '.join(notified_crops)}).")
    else:
        reasons.append(f"Crop '{profile.crop}' is eligible.")

    if rules.get("requires_irrigation_source", False) and not profile.has_irrigation_well:
        eligible = False
        reasons.append("Scheme requires an operational borewell or open well.")

    return SchemeMatchResult(
        scheme_id=scheme["scheme_id"],
        name=scheme["name"],
        category=scheme["category"],
        level=scheme["level"],
        eligible=eligible,
        reasons=reasons,
        benefits_summary=scheme["benefits_summary"],
        documents_required=scheme["documents_required"],
        deadlines=scheme["deadlines"],
        claim_window=scheme.get("claim_window"),
        source_url=scheme["source_url"],
        last_verified=scheme["last_verified"],
        where_to_apply=scheme["where_to_apply"]
    )

# Mock Farmer Database
MOCK_FARMERS_DB = [
    {
        "farmer_id": "F-TG-001",
        "farmer_name": "Komirelli Ramulu",
        "phone": "+91-98480-22338",
        "district": "Warangal",
        "village": "Geesugonda",
        "land_holding_acres": 2.2,
        "crop": "Paddy",
        "scheme_id": "TS-RB-01",
        "scheme_name": "Rythu Bharosa",
        "doc_status": "pending",
        "pending_documents": ["Aadhaar-Bank Name Match Affidavit"],
        "urgent_alert": "Rabi application window closing in 48 hours",
        "deadline_date": "2026-11-25",
        "days_left": 2,
        "aadhaar_name": "Komirelli Ramulu",
        "bank_account_name": "K. Ramulu",
        "name_match_status": "Requires Attention",
        "name_match_score": 82
    },
    {
        "farmer_id": "F-TG-002",
        "farmer_name": "Banoth Padma",
        "phone": "+91-94401-88219",
        "district": "Nalgonda",
        "village": "Miryalaguda",
        "land_holding_acres": 4.5,
        "crop": "Cotton",
        "scheme_id": "CEN-PMFBY-01",
        "scheme_name": "PMFBY Crop Insurance",
        "doc_status": "pending",
        "pending_documents": ["Sowing Certificate from AEO"],
        "urgent_alert": "Premium cut-off date is 15-Nov-2026",
        "deadline_date": "2026-11-15",
        "days_left": 10,
        "aadhaar_name": "Banoth Padma",
        "bank_account_name": "Guguloth Saroja",
        "name_match_status": "Severe Mismatch",
        "name_match_score": 40
    },
    {
        "farmer_id": "F-TG-003",
        "farmer_name": "Boda Venkanna",
        "phone": "+91-97011-33445",
        "district": "Khammam",
        "village": "Kallur",
        "land_holding_acres": 1.8,
        "crop": "Chilli",
        "scheme_id": "TS-TSMIP-01",
        "scheme_name": "TSMIP Drip Subsidy",
        "doc_status": "complete",
        "pending_documents": [],
        "urgent_alert": "Field inspection scheduled on Friday",
        "deadline_date": "2026-11-20",
        "days_left": 15,
        "aadhaar_name": "Boda Venkanna",
        "bank_account_name": "Boda Venkanna",
        "name_match_status": "Exact Match",
        "name_match_score": 100
    }
]

# API Endpoints
@app.get("/")
def read_root():
    return {
        "service": "Farmer Scheme Eligibility Assistant API",
        "version": "2.0.0",
        "pilot_state": "Telangana (Pan-India Supported)",
        "modules": [
            "Deterministic Scheme Matching",
            "72-Hour Crop Loss Claim Assistant",
            "Water-Saving Subsidy Matcher (18+ Schemes)",
            "Low-Water Crop Alternatives (26+ Crops)",
            "KCC Credit Calculator & 4% Subvention",
            "Document Wallet & DigiLocker",
            "Higher Official Grievance Escalation"
        ]
    }

@app.get("/schemes")
def get_all_schemes():
    return load_schemes()

@app.post("/match", response_model=MatchResponse)
def match_farmer_schemes(profile: FarmerProfile):
    schemes = load_schemes()
    eligible_list: List[SchemeMatchResult] = []
    ineligible_list: List[SchemeMatchResult] = []

    for scheme in schemes:
        res = evaluate_farmer(profile, scheme)
        if res.eligible:
            eligible_list.append(res)
        else:
            ineligible_list.append(res)

    return MatchResponse(
        profile=profile,
        eligible_schemes=eligible_list,
        ineligible_schemes=ineligible_list,
        total_eligible=len(eligible_list),
        evaluated_at=datetime.now().isoformat()
    )

@app.get("/farmer_status")
def get_intermediary_farmer_status(district: Optional[str] = None, doc_status: Optional[str] = None):
    results = MOCK_FARMERS_DB
    if district:
        results = [f for f in results if f["district"].lower() == district.lower()]
    if doc_status:
        results = [f for f in results if f["doc_status"].lower() == doc_status.lower()]
    return results

@app.get("/verify_name")
def verify_name_match(aadhaar_name: str, bank_name: str):
    clean_aadhaar = aadhaar_name.strip().lower().replace(".", " ")
    clean_bank = bank_name.strip().lower().replace(".", " ")
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

@app.get("/msp_comparison")
def get_msp_comparison():
    return [
        {"crop": "Paddy (Grade A)", "msp_rate": 2320, "state_bonus": 500, "effective_gov_price": 2820, "average_mandi_price": 2180, "price_delta": 640, "recommendation": "Sell at PACS / IKP procurement centre for +₹640/qtl bonus."},
        {"crop": "Cotton (Medium Staple)", "msp_rate": 7121, "state_bonus": 0, "effective_gov_price": 7121, "average_mandi_price": 6850, "price_delta": 271, "recommendation": "Sell at Cotton Corporation of India (CCI) centre."},
        {"crop": "Maize", "msp_rate": 2225, "state_bonus": 0, "effective_gov_price": 2225, "average_mandi_price": 2100, "price_delta": 125, "recommendation": "Sell at Markfed procurement centre."},
        {"crop": "Bengal Gram (Chana)", "msp_rate": 5440, "state_bonus": 0, "effective_gov_price": 5440, "average_mandi_price": 5100, "price_delta": 340, "recommendation": "Sell at NAFED / Markfed procurement centre."},
        {"crop": "Sesame (Til)", "msp_rate": 9267, "state_bonus": 0, "effective_gov_price": 9267, "average_mandi_price": 8700, "price_delta": 567, "recommendation": "Sell at Mandi with statutory MSP floor."}
    ]

@app.get("/climate_water_stress")
def get_climate_water_stress(district: str = "Warangal", state: Optional[str] = None, crop: str = "Paddy", water_source: str = "Borewell", lang: str = "en"):
    from utils.weather_api import get_live_weather, evaluate_multi_crop_climate_risk, generate_multilingual_water_advisory
    weather = get_live_weather(district, state=state)
    assessment = evaluate_multi_crop_climate_risk(weather, crop=crop, water_source=water_source)
    advisory_text = generate_multilingual_water_advisory(assessment, lang=lang)
    return {
        "weather": weather,
        "assessment": assessment,
        "advisory_text": advisory_text
    }

# New Endpoints for Full Feature Integration
@app.get("/water_saving_schemes")
def get_water_saving_schemes(state: Optional[str] = None):
    if not os.path.exists(WATER_SCHEMES_PATH):
        return []
    with open(WATER_SCHEMES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if state and state.lower() != "all":
        data = [s for s in data if "All States" in s.get("applicable_states", []) or state.lower() in [st.lower() for st in s.get("applicable_states", [])]]
    return data

@app.get("/low_water_crops")
def get_low_water_crops(category: Optional[str] = None):
    if not os.path.exists(LOW_WATER_CROPS_PATH):
        return []
    with open(LOW_WATER_CROPS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if category and category.lower() != "all":
        data = [c for c in data if category.lower() in c.get("category", "").lower()]
    return data

@app.get("/disaster_relief")
def get_disaster_relief_info():
    if not os.path.exists(DISASTER_RELIEF_PATH):
        return {}
    with open(DISASTER_RELIEF_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/calculate_kcc")
def api_calculate_kcc(req: KCCRequest):
    from utils.credit_kcc import calculate_kcc_eligibility
    return calculate_kcc_eligibility(crop=req.crop, land_acres=req.land_acres, existing_kcc_debt=req.existing_debt)

@app.post("/generate_claim_sms")
def api_generate_claim_sms(req: ClaimIntimationRequest):
    from utils.claim_assistant import generate_intimation_sms
    return generate_intimation_sms(
        farmer_name=req.farmer_name,
        phone=req.phone,
        crop=req.crop,
        district=req.district,
        village=req.village,
        survey_no=req.survey_no,
        loss_percent=req.loss_percent,
        hazard_type=req.hazard_type,
        acreage=req.acreage,
        language=req.language
    )

@app.get("/claims")
def api_get_claims():
    from utils.status_tracker import get_all_claims, compute_claim_urgency
    claims = get_all_claims()
    for c in claims:
        c["urgency_meta"] = compute_claim_urgency(c)
    return claims

@app.post("/claims")
def api_add_claim(req: ClaimEntryRequest):
    from utils.status_tracker import add_claim_entry
    return add_claim_entry(
        farmer_name=req.farmer_name,
        phone=req.phone,
        scheme_name=req.scheme_name,
        reference_number=req.reference_number,
        status=req.status,
        notes=req.notes or ""
    )

@app.post("/feedback")
def api_record_feedback(req: FeedbackRequest):
    from utils.escalation_feedback import record_feedback
    return record_feedback(
        scheme_id=req.scheme_id,
        scheme_name=req.scheme_name,
        feedback_type=req.feedback_type,
        reporter_role=req.reporter_role,
        description=req.description,
        state=req.state
    )

@app.post("/escalate")
def api_escalate_grievance(req: EscalationRequest):
    from utils.escalation_feedback import generate_formal_escalation_petition
    return generate_formal_escalation_petition(
        farmer_name=req.farmer_name,
        father_husband_name=req.father_husband_name,
        aadhaar_masked=req.aadhaar_masked,
        phone=req.phone,
        village=req.village,
        mandal=req.mandal,
        district=req.district,
        survey_no=req.survey_no,
        problem_category=req.problem_category,
        scheme_name=req.scheme_name,
        description=req.description,
        escalation_level=req.escalation_level
    )

@app.get("/documents")
def api_get_documents(farmer_id: str = "DEMO_FARMER_1"):
    from utils.document_wallet import get_farmer_documents
    return get_farmer_documents(farmer_id)
