import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from rapidfuzz import fuzz

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import domain modules
from engine import EligibilityEngine, check_eligibility as engine_check_eligibility
from person3.farmer_database import connect, init_db, get_db_path
from person3.farmer_profiles import (
    save_profile,
    get_profile,
    update_profile,
    list_all_farmers,
    search_farmer,
)
from person3.consent_manager import (
    validate_consent,
    get_consent_terms,
    withdraw_consent,
    grant_consent,
    is_consent_active,
)
from person3.document_checker import check_name_match, check_documents
from person3.intermediary_backend import get_intermediary_farmers
from utils.claim_assistant import calculate_72hr_window, generate_intimation_sms, PMFBY_HELPLINE
from utils.credit_kcc import calculate_kcc_eligibility
from utils.status_tracker import get_all_claims, add_claim_entry
from utils.llm import process_farmer_query

app = FastAPI(
    title="OpenQuest - Unified Public Agritech & Scheme Assistant API",
    description="Deterministic rule-based eligibility engine, consent vault, KCC calculator, 72-hour claim assistant, and SQLite-backed intermediary mode.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(str(PROJECT_ROOT), "data", "schemes_telangana.json")
PAN_INDIA_SCHEMES_PATH = os.path.join(str(PROJECT_ROOT), "schemes.json")
WATER_SCHEMES_PATH = os.path.join(str(PROJECT_ROOT), "data", "water_saving_schemes.json")
LOW_WATER_CROPS_PATH = os.path.join(str(PROJECT_ROOT), "data", "low_water_crops.json")
FRONTEND_DIR = os.path.join(str(PROJECT_ROOT), "frontend")

def load_schemes() -> List[Dict[str, Any]]:
    """Loads Telangana schemes for test compatibility and pilot validation."""
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Pydantic Models
class FarmerProfile(BaseModel):
    farmer_id: Optional[str] = "F-TEMP"
    name: Optional[str] = "Farmer"
    farmer_name: Optional[str] = None
    state: str = "Telangana"
    district: Optional[str] = "Warangal"
    land_holding_acres: float = Field(default=2.0, ge=0.0)
    land_acres: Optional[float] = None
    crop: str = "Paddy"
    crops: Optional[List[str]] = None
    category: str = "marginal"  # marginal (<2.5 acres), small (2.5-5 acres), tenant, medium, large
    is_tenant: bool = False
    has_ccrc: bool = False  # Crop Cultivator Rights Card for tenant
    has_rofr_patta: bool = False
    caste_category: Optional[str] = "BC"  # SC, ST, BC, General
    has_irrigation_well: bool = True
    age: int = 40
    is_tax_payer: bool = False
    query: Optional[str] = None
    language: Optional[str] = "en"  # en, te, hi, mr, ta

class SchemeMatchResult(BaseModel):
    scheme_id: str
    name: str
    category: str
    level: str
    eligible: bool
    reasons: List[str]
    benefits_summary: str
    documents_required: List[str]
    deadlines: Union[Dict[str, Any], str]
    claim_window: Optional[Union[Dict[str, Any], str]] = None
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

class ClaimDispatchRequest(BaseModel):
    farmer_name: str
    farmer_id: Optional[str] = "F-NEW"
    phone: str
    state: str = "Telangana"
    district: str = "Warangal"
    village: str = "Geesugonda"
    survey_no: str = "402/A"
    crop: str = "Paddy"
    calamity_cause: str = "Hailstorm"
    loss_percentage: int = 75
    incident_date: Optional[str] = None
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

class KCCRequest(BaseModel):
    crop: str = "Paddy"
    land_acres: float = 2.5
    existing_debt: float = 0.0

class QueryAIRequest(BaseModel):
    query: str
    language: str = "en"

# Deterministic Evaluation Engine for Telangana Schemes
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
    effective_land = profile.land_acres if profile.land_acres is not None else profile.land_holding_acres
    min_land = rules.get("min_land_acres")
    max_land = rules.get("max_land_acres")
    if min_land is not None and effective_land < min_land:
        eligible = False
        reasons.append(f"Minimum land required is {min_land} acres (you entered {effective_land} acres).")
    if max_land is not None and effective_land > max_land:
        eligible = False
        reasons.append(f"Maximum land permissible is {max_land} acres (you entered {effective_land} acres).")

    # Rule 3: Tenant & Land Title Rules
    if rules.get("requires_land_title_or_ccrc", False):
        if profile.is_tenant:
            if not profile.has_ccrc and scheme.get("scheme_id") == "TS-RB-01":
                eligible = False
                reasons.append("Tenant farmers require Crop Cultivator Rights Card (CCRC) for Rythu Bharosa.")
            elif profile.has_ccrc:
                reasons.append("Tenant eligibility verified via CCRC endorsement.")
        else:
            reasons.append("Landownership title required (Pattadar / Dharani RoR).")

    # Rule 4: Crop Specificity
    allowed_crops = rules.get("allowed_crops")
    effective_crop = profile.crop
    if profile.crops and len(profile.crops) > 0:
        effective_crop = profile.crops[0]
    if allowed_crops:
        if effective_crop.strip().title() not in [c.title() for c in allowed_crops]:
            eligible = False
            reasons.append(f"Scheme is for crops: {', '.join(allowed_crops)}. Your crop is {effective_crop}.")
        else:
            reasons.append(f"Crop '{effective_crop}' is eligible under this notification.")

    # Rule 5: Infrastructure
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

# Sample database of farmers for fallback and test compliance
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

def init_sqlite_seed_data():
    """Initializes SQLite database and populates with initial farmer profiles if empty."""
    init_db()
    existing_farmers = list_all_farmers()
    if len(existing_farmers) < 4:
        seed_profiles = [
            {
                "farmer_id": "DEMO_F001",
                "farmer_name": "Ravi Kumar",
                "phone_number": "9876543210",
                "preferred_language": "te",
                "intermediary_id": "CSC_WARANGAL_01",
                "consent_status": True,
                "uploaded_documents": {"Aadhaar": True, "Bank Passbook": False, "Land Records": True},
                "bank_account_name": "Ravi Kumer",
            },
            {
                "farmer_id": "TS-WAR-001",
                "farmer_name": "Komirelli Ramulu",
                "phone_number": "9848012345",
                "preferred_language": "te",
                "intermediary_id": "CSC_WARANGAL_01",
                "consent_status": True,
                "uploaded_documents": {"Aadhaar": True, "Bank Passbook": True, "Sowing Certificate": False},
                "bank_account_name": "K. Ramulu",
            },
            {
                "farmer_id": "TS-KHM-003",
                "farmer_name": "Banoth Padma",
                "phone_number": "9701234567",
                "preferred_language": "te",
                "intermediary_id": "CSC_KHAMMAM_01",
                "consent_status": True,
                "uploaded_documents": {"Aadhaar": True, "Crop Damage Photos": True, "Bank Passbook": False},
                "bank_account_name": "Padma B",
            },
            {
                "farmer_id": "TS-NAL-002",
                "farmer_name": "Boda Venkanna",
                "phone_number": "9440123456",
                "preferred_language": "te",
                "intermediary_id": "CSC_NALGONDA_02",
                "consent_status": True,
                "uploaded_documents": {"Aadhaar": True, "Bank Passbook": True, "Land Records": True},
                "bank_account_name": "Boda Venkanna",
            },
            {
                "farmer_id": "TS-NZB-004",
                "farmer_name": "Mohammad Shabbir",
                "phone_number": "9866098765",
                "preferred_language": "te",
                "intermediary_id": "CSC_NIZAMABAD_03",
                "consent_status": True,
                "uploaded_documents": {"Aadhaar": True, "Electricity Bill": False},
                "bank_account_name": "Mohd Shabbir",
            }
        ]
        for p in seed_profiles:
            try:
                save_profile(p)
            except Exception:
                pass

@app.on_event("startup")
def startup_event():
    init_sqlite_seed_data()

# API Endpoints

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OpenQuest Civic Agritech Engine",
        "database": "SQLite (database/farmer_data.db)",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/match", response_model=MatchResponse)
def match_schemes(profile: FarmerProfile):
    """Deterministic eligibility matching across verified schemes."""
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

@app.post("/api/match")
def match_pan_india_schemes(payload: Dict[str, Any] = Body(...)):
    """
    Pan-India & State-specific Deterministic Scheme Matcher (32+ schemes).
    Evaluates against all 29 Indian States using verified statutory rules.
    """
    state = payload.get("state", "Telangana")
    land_acres = float(payload.get("land_acres", payload.get("land_holding_acres", 2.0)))
    is_tenant = bool(payload.get("is_tenant", False))
    has_rofr = bool(payload.get("has_rofr_patta", False))
    crops_input = payload.get("crops", payload.get("crop", "Paddy"))
    crops = [c.strip() for c in crops_input.split(",")] if isinstance(crops_input, str) else list(crops_input)
    age = int(payload.get("age", 40))
    is_tax_payer = bool(payload.get("is_tax_payer", False))

    engine = EligibilityEngine(PAN_INDIA_SCHEMES_PATH)
    profile_dict = {
        "farmer_name": payload.get("farmer_name", payload.get("name", "Farmer")),
        "state": state,
        "district": payload.get("district", "Warangal"),
        "land_acres": land_acres,
        "is_tenant": is_tenant,
        "has_rofr_patta": has_rofr,
        "crops": crops,
        "age": age,
        "is_tax_payer": is_tax_payer
    }

    results = engine.check_eligibility(profile_dict)
    eligible = [s for s in results if s["eligible"]]
    ineligible = [s for s in results if not s["eligible"]]

    total_direct_cash = 0.0
    for s in eligible:
        sid = s.get("scheme_id")
        if sid in ["rythu_bharosa", "ts_rythu_bharosa"]:
            total_direct_cash += 15000.0 * min(land_acres, 10.0)
        elif sid == "pm_kisan":
            total_direct_cash += 6000.0
        elif sid == "ap_annadata_sukhibhava":
            total_direct_cash += 20000.0
        elif sid == "mh_namo_shetkari":
            total_direct_cash += 6000.0
        elif sid == "kalia":
            total_direct_cash += 10000.0

    return {
        "status": "success",
        "state": state,
        "total_evaluated": len(results),
        "total_eligible": len(eligible),
        "total_ineligible": len(ineligible),
        "total_direct_cash_annual": total_direct_cash,
        "eligible_schemes": eligible,
        "ineligible_schemes": ineligible,
        "profile": profile_dict,
        "evaluated_at": datetime.now().isoformat()
    }

@app.post("/verify_name_match")
@app.post("/api/verify_name_match")
def verify_name_match(aadhaar_name: str = Body(..., embed=True), bank_name: str = Body(..., embed=True)):
    """Fuzzy match between Aadhaar name and Bank account name using RapidFuzz."""
    clean_aadhaar = aadhaar_name.strip().lower().replace(".", " ")
    clean_bank = bank_name.strip().lower().replace(".", " ")
    ratio = int(fuzz.token_set_ratio(clean_aadhaar, clean_bank))
    status = "Exact Match" if ratio == 100 else ("Minor Variation" if ratio >= 80 else "Severe Mismatch")
    return {
        "aadhaar_name": aadhaar_name,
        "bank_name": bank_name,
        "similarity_score": ratio,
        "status": status,
        "requires_manual_verification": ratio < 100,
        "action_required": "None (Ready for DBT)" if ratio >= 80 else "Visit Bank branch or CSC with Aadhaar to update name."
    }

@app.post("/api/consent/toggle")
def toggle_consent(farmer_id: str = Body(..., embed=True)):
    """Toggles or revokes farmer consent in SQLite database."""
    farmer = get_profile(farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer profile not found in database")
    current_status = bool(farmer.get("consent_status", False))
    new_status = not current_status
    if new_status:
        grant_consent(farmer_id)
    else:
        withdraw_consent(farmer_id)
    return {
        "status": "success",
        "farmer_id": farmer_id,
        "consent_status": new_status,
        "message": "Consent active" if new_status else "Consent revoked. Personal data masked."
    }

@app.get("/farmer_status")
@app.get("/api/farmers")
def get_farmer_status(district: Optional[str] = None, doc_status: Optional[str] = None):
    """Intermediary mode API: Fetches farmers with pending documents and approaching deadlines."""
    farmers = MOCK_FARMERS_DB
    if district and district.lower() != "all":
        farmers = [f for f in farmers if f["district"].lower() == district.lower()]
    if doc_status and doc_status.lower() != "all":
        farmers = [f for f in farmers if f["doc_status"].lower() == doc_status.lower()]
    return farmers

@app.get("/api/intermediary")
def get_intermediary_dashboard(intermediary_id: Optional[str] = None):
    """SQLite-driven CSC & Village Operator Task Queue."""
    schemes = load_schemes()
    task_queue = get_intermediary_farmers(scheme_data=schemes, today=date.today(), intermediary_id=intermediary_id)
    return {
        "status": "success",
        "total_records": len(task_queue),
        "records": task_queue
    }

@app.post("/api/farmers")
def create_farmer_profile(profile: Dict[str, Any] = Body(...)):
    """Saves new farmer profile to SQLite database with consent verification."""
    try:
        saved = save_profile(profile)
        return {"status": "success", "profile": saved}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/send_alert")
@app.post("/api/send_alert")
def send_proactive_alert(req: AlertRequest):
    """Sends / simulates proactive deadline alert to the farmer."""
    farmer = next((f for f in MOCK_FARMERS_DB if f["farmer_id"] == req.farmer_id), None)
    if not farmer:
        farmer_sql = get_profile(req.farmer_id)
        if farmer_sql:
            farmer = {
                "farmer_id": farmer_sql["farmer_id"],
                "farmer_name": farmer_sql["farmer_name"],
                "phone": farmer_sql.get("phone_number", "+91 98480 00000")
            }
        else:
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

@app.post("/api/kcc/calculate")
def calculate_kcc(req: KCCRequest):
    """Calculates KCC Scale of Finance, collateral limits, and 4% MISS net interest rate."""
    result = calculate_kcc_eligibility(
        crop=req.crop,
        land_acres=req.land_acres,
        existing_kcc_debt=req.existing_debt
    )
    return {
        "status": "success",
        "data": result
    }

@app.post("/api/claim/dispatch")
def dispatch_emergency_claim(req: ClaimDispatchRequest):
    """
    Submits emergency 72-hour crop loss intimation.
    Generates statutory docket reference number and formatted SMS string.
    """
    docket_num = f"PMFBY/{req.state[:2].upper()}/2026/{int(datetime.now().timestamp()) % 1000000:06d}"
    sms_string = f"CLAIM {req.village.upper()} {req.survey_no} {req.loss_percentage}% {req.calamity_cause.upper()}"
    
    # Store into claims tracker
    add_claim_entry(
        farmer_name=req.farmer_name,
        phone=req.phone,
        scheme_name="PMFBY 72-Hour Emergency Claim",
        reference_number=docket_num,
        status="Loss Intimation Received (SLA: 72 Hours)",
        notes=f"Survey: {req.survey_no}, Cause: {req.calamity_cause}, Loss: {req.loss_percentage}%. {req.notes}",
        filing_date_str=datetime.now().strftime("%Y-%m-%d")
    )

    return {
        "status": "dispatched",
        "docket_number": docket_num,
        "farmer_name": req.farmer_name,
        "sms_string": sms_string,
        "target_gateway": "51969",
        "pmfby_toll_free": PMFBY_HELPLINE,
        "statutory_window": "72 Hours from loss event",
        "next_step": "AEO will conduct field verification with Joint Survey Team within 15 days.",
        "dispatched_at": datetime.now().isoformat()
    }

@app.get("/api/claims")
def list_claims():
    """Lists all active and tracked claims."""
    claims = get_all_claims()
    return {"status": "success", "claims": claims}

@app.get("/msp_comparison")
@app.get("/api/msp_comparison")
def get_msp_comparison():
    """Live MSP vs APMC Mandi Benchmark dataset with routing recommendations."""
    return [
        {
            "crop": "Sesame (Til / Nuvvulu)",
            "category": "Oilseed (Resilient)",
            "msp_rate": 9267,
            "state_bonus": 0,
            "effective_gov_price": 9267,
            "average_mandi_price": 8850,
            "price_delta": -417,
            "recommendation": "Sell at government PACS / NAFED procurement center to gain +₹417/quintal over open market.",
            "source": "NAFED e-Procurement Portal"
        },
        {
            "crop": "Green Gram (Moong)",
            "category": "Pulse (60-Day)",
            "msp_rate": 8682,
            "state_bonus": 0,
            "effective_gov_price": 8682,
            "average_mandi_price": 8920,
            "price_delta": 238,
            "recommendation": "Sell in Open APMC Mandi. Current auction price is ₹238 above statutory MSP.",
            "source": "Agmarknet APMC Auction Feed"
        },
        {
            "crop": "Bengal Gram (Chana)",
            "category": "Rabi Pulse",
            "msp_rate": 5440,
            "state_bonus": 0,
            "effective_gov_price": 5440,
            "average_mandi_price": 5120,
            "price_delta": -320,
            "recommendation": "Sell at FCI / PACS center. Open trader price is discounted by ₹320.",
            "source": "FCI Regional Procurement"
        },
        {
            "crop": "Soybean (Yellow)",
            "category": "Kharif Commercial",
            "msp_rate": 4892,
            "state_bonus": 0,
            "effective_gov_price": 4892,
            "average_mandi_price": 4450,
            "price_delta": -442,
            "recommendation": "Utilize e-NWR Warehouse Pledge financing to defer sale until post-harvest recovery.",
            "source": "WDRA / e-NAM Warehouse Pledge"
        },
        {
            "crop": "Paddy (Common / Grade A)",
            "category": "Cereal",
            "msp_rate": 2320,
            "state_bonus": 500,
            "effective_gov_price": 2820,
            "average_mandi_price": 2180,
            "price_delta": 640,
            "recommendation": "Sell at government IKP / PACS procurement centre to gain +₹640/quintal over open market.",
            "source": "Civil Supplies Corporation"
        },
        {
            "crop": "Cotton (Medium Staple)",
            "category": "Commercial Fiber",
            "msp_rate": 7121,
            "state_bonus": 0,
            "effective_gov_price": 7121,
            "average_mandi_price": 6850,
            "price_delta": 271,
            "recommendation": "Sell to Cotton Corporation of India (CCI) procurement center at MSP of ₹7,121.",
            "source": "Cotton Corporation of India (CCI)"
        }
    ]

@app.get("/api/water_subsidies")
def get_water_subsidies():
    """Lists diversified water-saving subsidies (18+ schemes across India)."""
    if os.path.exists(WATER_SCHEMES_PATH):
        with open(WATER_SCHEMES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.get("/api/resilient_crops")
def get_resilient_crops():
    """Lists resilient low-water crops (26+ crops)."""
    if os.path.exists(LOW_WATER_CROPS_PATH):
        with open(LOW_WATER_CROPS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

import json
import os
import sys

def get_farmer_ai_response(query_text: str, language: str = "en") -> dict:
    q = query_text.strip().lower()
    lang = language.lower() if language in ["en", "te", "hi"] else "en"

    # Intent 1: Documents & Proofs required
    if any(k in q for k in ["doc", "document", "documents", "proof", "paper", "పత్రాలు", "దస్తావేజులు", "కాగితాలు", "दस्तावेज", "कागजात"]):
        if lang == "te":
            msg = (
                "📋 **రైతు సంక్షేమ పథకాలకు అవసరమైన ముఖ్యమైన పత్రాల జాబితా (Document Checklist)**:\n\n"
                "1. **ఆధార్ కార్డు (Aadhaar Card)**: క్రియాశీల మొబైల్ నంబర్‌తో లింక్ చేయబడి ఉండాలి (e-KYC కోసం).\n"
                "2. **భూమి రికార్డు (Land Record / 1B / Pahani)**: సర్వే నంబర్, విస్తీర్ణం తెలిపే డిజిటల్ పట్టాదారు పాస్‌బుక్ లేదా ధరణి / పహాణీ నకలు.\n"
                "3. **బ్యాంక్ పాస్‌బుక్ (Bank Passbook)**: ఆధార్‌తో అనుసంధానించబడిన (NPCI DBT Seeded) బ్యాంక్ ఖాతా.\n"
                "4. **కౌలు సాగు హక్కు కార్డు (CCRC)**: కౌలు రైతులకు మాత్రమే - ఆర్డీవో / తహసీల్దార్ జారీ చేసిన పంట సాగు హక్కు పత్రం.\n"
                "5. **విత్తన / సాగు ధృవీకరణ పత్రం (Sowing Certificate)**: స్థానిక వ్యవసాయ విస్తరణ అధికారి (AEO) లేదా రైతు వేదిక ద్వారా జారీ చేయబడుతుంది.\n"
                "6. **పాస్‌పోర్ట్ సైజు ఫోటోలు**: 2 తాజా రంగు ఫోటోలు.\n\n"
                "💡 **చిట్కా**: ఈ పత్రాలను మీరు మా **Tab 5 (Document Wallet)** లో భద్రపరుచుకోవచ్చు. మీ ఆధార్ నంబర్ `XXXX-XXXX-4921` రూపంలో గోప్యంగా దాచబడుతుంది."
            )
        elif lang == "hi":
            msg = (
                "📋 **कृषि योजनाओं एवं सब्सिडी हेतु आवश्यक दस्तावेजों की सूची (Document Checklist)**:\n\n"
                "1. **आधार कार्ड (Aadhaar Card)**: सक्रिय मोबाइल नंबर से लिंक (e-KYC प्रमाणीकरण हेतु)।\n"
                "2. **भू-अभिलेख (खतौनी / खसरा / Pahani / RoR-1B)**: सर्वे नंबर एवं रकबा स्पष्ट करने वाली नकल।\n"
                "3. **बैंक पासबुक (Bank Passbook)**: आधार से जुड़ा (NPCI DBT सक्षम) चालू बैंक खाता।\n"
                "4. **बटाईदार प्रमाण पत्र (CCRC / Lease)**: काश्तकार या बटाईदार किसानों के लिए वैध अनुबंध।\n"
                "5. **बुवाई प्रमाण पत्र (Sowing Certificate)**: क्षेत्रीय कृषि अधिकारी (AEO / पटवारी) द्वारा जारी।\n"
                "6. **पासपोर्ट साइज फोटो**: 2 हालिया पासपोर्ट तस्वीरें।\n\n"
                "💡 **सुझाव**: आप इन दस्तावेजों को सुरक्षित रूप से **Tab 5 (Document Wallet)** में सेव कर सकते हैं, जहां आधार नंबर `XXXX-XXXX-4921` के रूप में सुरक्षित रहेगा।"
            )
        else:
            msg = (
                "📋 **Standard Required Documents for Agricultural Schemes & Subsidies**:\n\n"
                "1. **Aadhaar Card**: Must be linked to an active mobile number for OTP e-KYC authentication.\n"
                "2. **Land Ownership Title (Pahani / Dharani / Khasra / RoR-1B)**: Digital passbook showing Survey Number and Khata extent.\n"
                "3. **Bank Account Passbook**: Must be Aadhaar-seeded on NPCI mapper for Direct Benefit Transfer (DBT).\n"
                "4. **Crop Cultivator Rights Card (CCRC)**: Mandatory for tenant farmers / sharecroppers (ensures rights without impacting landowner title).\n"
                "5. **Sowing Certificate / Girdawari**: Issued by local Agriculture Extension Officer (AEO) / Rythu Vedika.\n"
                "6. **Passport Size Photographs**: 2 recent color photographs.\n\n"
                "💡 **Pro-Tip**: You can safely store these in **Tab 5 (Document Wallet)** with automatic privacy masking (`XXXX-XXXX-4921`)."
            )
        return {
            "status": "success",
            "query": query_text,
            "response": msg,
            "action": "view_wallet",
            "url": "#doc-wallet"
        }

    # Intent 2: 72-Hour Claim Window & Crop Insurance
    if any(k in q for k in ["72", "claim", "loss", "damage", "hail", "flood", "cyclone", "insurance", "pmfby", "నష్టం", "పరిహారం", "బీమా", "नुकसान", "बीमा", "मुआवजा"]):
        if lang == "te":
            msg = (
                "⏱️ **పీఎంఎఫ్‌బీవై 72 గంటల అత్యవసర నష్ట పరిహార నిబంధన (PMFBY 72-Hour Rule)**:\n\n"
                "• స్థానికీకరించిన విపత్తులు (వడగండ్ల వాన, వరదలు, కొండచరియలు) సంభవించినప్పుడు **72 గంటల లోపు తప్పనిసరిగా** సమాచారం అందించాలి.\n"
                "• **టోల్ ఫ్రీ హెల్ప్‌లైన్**: `1800-180-1551` లేదా మీ మండల ఏఈఓ (AEO) / రైతు వేదికకు లిఖితపూర్వక దరఖాస్తు ఇవ్వండి.\n"
                "• **సాక్ష్యం**: జీపీఎస్ లొకేషన్ (Geo-Tagged) ఆన్ చేసి దెబ్బతిన్న పంట ఫోటోలు తీయండి.\n"
                "• **ఎస్‌డీఆర్‌ఎఫ్ సహాయం**: వర్షాధార పంటలకు ₹8,500/హెక్టారు, నీటిపారుదల పంటలకు ₹17,000/హెక్టారు రాష్ట్ర విపత్తు నిధి ద్వారా అదనంగా లభిస్తుంది.\n\n"
                "👉 మా **Tab 2 (72-Hr Claim Shield)** లో 1-క్లిక్ ద్వారా అధికారిక ఎస్ఎంఎస్ (SMS) జనరేట్ చేసుకోవచ్చు!"
            )
        else:
            msg = (
                "⏱️ **PMFBY Statutory 72-Hour Crop Loss Reporting Rule**:\n\n"
                "• Under PMFBY Section 21.4, localized calamities (Hailstorm, Inundation, Cloudburst, Landslide) MUST be reported **within 72 hours** of occurrence.\n"
                "• **Toll-Free Helpline**: Call **1800-180-1551** immediately and obtain a Docket Reference ID.\n"
                "• **Field Photos**: Take minimum 3 geo-tagged GPS photos showing damaged field and survey boundaries.\n"
                "• **SDRF Calamity Norms**: In addition to insurance, eligible farmers receive State Disaster Relief (Rainfed: ₹8,500/ha; Irrigated: ₹17,000/ha; Perennial: ₹22,500/ha).\n\n"
                "👉 Use **Tab 2 (72-Hr Claim Shield)** to start the live countdown and generate a 1-click legal SMS intimation!"
            )
        return {
            "status": "success",
            "query": query_text,
            "response": msg,
            "action": "view_claim_shield",
            "url": "#claim-shield"
        }

    # Intent 3: KCC Loan & 4% Interest Subvention
    if any(k in q for k in ["kcc", "loan", "interest", "credit", "scale of finance", "వడ్డీ", "రుణం", "కిసాన్ క్రెడిట్", "कर्ज", "ब्याज"]):
        if lang == "te":
            msg = (
                "🏦 **కిసాన్ క్రెడిట్ కార్డు (KCC) & 4% వడ్డీ రాయితీ పథకం (MISS)**:\n\n"
                "• ప్రామాణిక బ్యాంక్ వ్యవసాయ రుణ వడ్డీ రేటు: **7.0%** (రూ. 3 లక్షల వరకు).\n"
                "• సకాలంలో చెల్లింపు ప్రోత్సాహకం (PRI): **- 3.0%** (ప్రభుత్వమే భరిస్తుంది).\n"
                "• **రైతు నికర వడ్డీ రేటు**: ఏడాదికి కేవలం **4.0%** మాత్రమే!\n"
                "• తనఖా లేని రుణం (Collateral-Free): భూమి తాకట్టు లేకుండా **రూ. 1.60 లక్షల వరకు** లభిస్తుంది.\n"
                "• స్కేల్ ఆఫ్ ఫైనాన్స్: వరి సాగుకు ఎకరానికి ~₹38,000, పత్తికి ~₹42,000, మిర్చికి ~₹65,000 వరకు రుణం మంజూరవుతుంది.\n\n"
                "👉 మా **Tab 4 (KCC Loan & Tracker)** లో మీ పంట మరియు భూమికి అర్హమైన ఖచ్చితమైన రుణ మొత్తాన్ని లెక్కించండి!"
            )
        else:
            msg = (
                "🏦 **Kisan Credit Card (KCC) & 4% Interest Subvention (MISS)**:\n\n"
                "• **Standard Bank Crop Loan Rate**: 7.0% per annum (up to ₹3.00 Lakh).\n"
                "• **Prompt Repayment Incentive (PRI)**: - 3.0% discount credited by Central Govt.\n"
                "• **Net Effective Farmer Interest**: Only **4.0% per annum** when repaid on schedule.\n"
                "• **Collateral-Free Limit**: Up to ₹1.60 Lakh sanctioned without land hypothecation.\n"
                "• **Scale of Finance**: Paddy ~₹38,000/acre, Cotton ~₹42,000/acre, Chilli ~₹65,000/acre.\n"
                "• **Repayment Due Dates**: Kharif loans due by March 31; Rabi loans due by June 30.\n\n"
                "👉 Head to **Tab 4 (KCC Loan & Tracker)** to compute your exact sanctioned limit and track pending files!"
            )
        return {
            "status": "success",
            "query": query_text,
            "response": msg,
            "action": "view_kcc",
            "url": "#kcc-tracker"
        }

    # Intent 4: Tenant Farmers & CCRC
    if any(k in q for k in ["ccrc", "tenant", "lease", "sharecropper", "oral", "కౌలు", "బట్టీ", "काश्तकार", "बटाईदार"]):
        if lang == "te":
            msg = (
                "🤝 **కౌలు రైతుల హక్కులు మరియు CCRC కార్డు మార్గదర్శకాలు**:\n\n"
                "• **CCRC (పంట సాగుదారుల హక్కుల కార్డు)**: కౌలు రైతులకు పంట కాలానికి (11 నెలలు) చట్టపరమైన గుర్తింపునిస్తుంది.\n"
                "• **భూ యజమాని భద్రత**: CCRC వలన భూమి యాజమాన్య హక్కులపై ఎలాంటి ప్రభావం పడదు. పట్టాదారు హక్కులు 100% సురక్షితం.\n"
                "• **కౌలు రైతు పొందే ప్రయోజనాలు**: పంట నష్ట పరిహారం (PMFBY), రాయితీ విత్తనాలు, మరియు ప్రభుత్వ పంట కొనుగోలు (MSP).\n"
                "• **ఎలా పొందాలి**: గ్రామ వ్యవసాయ విస్తరణ అధికారి (AEO) లేదా తహసీల్దార్ వద్ద ఉమ్మడి దరఖాస్తు సమర్పించాలి."
            )
        else:
            msg = (
                "🤝 **Tenant Farmer Protections & Crop Cultivator Rights Card (CCRC)**:\n\n"
                "• **What is CCRC?** A statutory agreement (valid for 11 months) recognizing tenant cultivators.\n"
                "• **Landowner Protection**: CCRC does NOT grant any ownership claim or tenancy encumbrance on land records. Land title remains 100% secure with the Pattadar.\n"
                "• **Benefits for Tenant**: Unlocks institutional crop insurance (PMFBY), disaster input subsidy, and official MSP procurement at government centres.\n"
                "• **How to Apply**: Joint declaration signed by tenant and landowner, verified by Village Revenue Officer / AEO."
            )
        return {
            "status": "success",
            "query": query_text,
            "response": msg,
            "action": "info",
            "url": "#tenant-ccrc"
        }

    # Intent 5: Water Saving & Drip Subsidies
    if any(k in q for k in ["water", "drip", "sprinkler", "solar", "kusum", "pmksy", "tsmip", "pond", "borewell", "నీరు", "డ్రిప్", "స్ప్రింక్లర్", "సోలార్", "ड्रिप", "सिंचाई"]):
        if lang == "te":
            msg = (
                "💧 **సూక్ష్మ సేద్యం మరియు నీటి సంరక్షణ రాయితీలు (18+ పథకాలు)**:\n\n"
                "• **తెలంగాణ TSMIP**: ఎస్సీ/ఎస్టీ రైతులకు **100% ఉచిత సబ్సిడీ**, బీసీ రైతులకు **90% సబ్సిడీ**, ఇతర రైతులకు **80% సబ్సిడీ**.\n"
                "• **పీఎం-కుసుమ్ (PM-KUSUM Component B)**: వ్యవసాయ సోలార్ పంపు సెట్లకు **60% వరకు సబ్సిడీ**.\n"
                "• **తక్కువ నీటి పంటలు**: వరి స్థానంలో శనగలు (-83% నీరు), నువ్వులు (-87% నీరు), లేదా జొన్నలు/సజ్జలు (-88% నీరు) సాగు చేస్తే గరిష్ట ఆదాయం లభిస్తుంది.\n\n"
                "👉 పూర్తి వివరాల కోసం మా **Tab 3 (Water Subsidies & Crops)** పరిశీలించండి!"
            )
        else:
            msg = (
                "💧 **Micro-Irrigation & Water-Saving Subsidies (18+ Schemes Across India)**:\n\n"
                "• **PMKSY Per Drop More Crop (PDMC)**: Baseline 55% Central subsidy for drip & sprinkler systems.\n"
                "• **State Enhancements**: Telangana (TSMIP) & AP (APMIP) provide up to **100% subsidy for SC/ST** and **90% for BC** small farmers.\n"
                "• **PM-KUSUM Component B**: 60% combined subsidy on standalone off-grid DC solar irrigation pumps.\n"
                "• **Next-Season Crop Planning**: Switching to Bengal Gram, Sesame, or Millets saves up to **88% water** compared to inundated paddy with assured MSP floor prices.\n\n"
                "👉 Browse all 18 schemes and 26 drought-resilient crops in **Tab 3 (Water Subsidies & Crops)**!"
            )
        return {
            "status": "success",
            "query": query_text,
            "response": msg,
            "action": "view_water",
            "url": "#water-subsidies"
        }

    # Intent 6: PM-KISAN & Rythu Bharosa
    if any(k in q for k in ["pm kisan", "pm-kisan", "pmkisan", "2000", "installment", "rythu bharosa", "రైతు భరోసా", "పీఎం కిసాన్", "किस्त"]):
        if lang == "te":
            msg = (
                "🌾 **పీఎం-కిసాన్ & రైతు భరోసా పెట్టుబడి సాయం**:\n\n"
                "• **పీఎం-కిసాన్ (PM-KISAN)**: ఏడాదికి ₹6,000 (మూడు విడతల్లో ₹2,000 చొప్పున నేరుగా బ్యాంక్ ఖాతాలో జమ).\n"
                "• **రైతు భరోసా (తెలంగాణ)**: అర్హులైన రైతులకు ఎకరానికి ఏడాదికి ₹15,000 పెట్టుబడి సహాయం.\n"
                "• **e-KYC అవసరం**: pmkisan.gov.in పోర్టల్‌లో బయోమెట్రిక్ లేదా ఓటీపీ ద్వారా ఆధార్ e-KYC తప్పనిసరి.\n"
                "• చెల్లింపు సమస్యల పరిష్కారానికి అధికారిక కిసాన్ ఈ-మిత్ర (Kisan e-Mitra AI) లేదా 155261 హెల్ప్‌లైన్‌ను సంప్రదించండి."
            )
        else:
            msg = (
                "🌾 **Direct Income Support Schemes (PM-KISAN & Rythu Bharosa)**:\n\n"
                "• **PM-KISAN**: ₹6,000 per year paid in 3 four-monthly installments of ₹2,000 each via DBT.\n"
                "• **Rythu Bharosa (Telangana)**: ₹15,000 per acre per year direct investment assistance for eligible farmers.\n"
                "• **Mandatory e-KYC**: Must be completed via Aadhaar OTP on pmkisan.gov.in or biometric CSC.\n"
                "• **Inquiries**: For pending installments, use the official Kisan e-Mitra AI chatbot at pmkisan.gov.in or call Helpline 155261."
            )
        return {
            "status": "success",
            "query": query_text,
            "response": msg,
            "action": "redirect",
            "url": "https://pmkisan.gov.in"
        }

    # Intent 7: MSP vs Mandi prices
    if any(k in q for k in ["msp", "mandi", "price", "bonus", "ధర", "మద్దతు", "भाव", "मंडी"]):
        if lang == "te":
            msg = (
                "⚖️ **కనీస మద్దతు ధర (MSP) & మార్కెట్ ధరలు (2025-2026)**:\n\n"
                "• **వరి (గ్రేడ్-ఏ)**: కేంద్ర MSP ₹2,320 + తెలంగాణ ప్రత్యేక బోనస్ ₹500 = **మొత్తం ₹2,820/క్వింటాల్**.\n"
                "• **పత్తి**: MSP ₹7,121/క్వింటాల్ (సీసీఐ కొనుగోలు కేంద్రాల్లో అమ్మడం లాభదాయకం).\n"
                "• **మొక్కజొన్న**: MSP ₹2,225/క్వింటాల్.\n"
                "• దళారులకు తక్కువ ధరకు విక్రయించవద్దు. నేరుగా పీఏసీఎస్ (PACS) లేదా ఐకేపీ (IKP) కొనుగోలు కేంద్రాల్లో విక్రయించండి."
            )
        else:
            msg = (
                "⚖️ **Minimum Support Price (MSP) & Market Arbitrage (2025-2026)**:\n\n"
                "• **Paddy (Grade A)**: Statutory MSP ₹2,320 + Telangana State Bonus ₹500 = **Effective ₹2,820/qtl** (Private mandi pays ~₹2,180; net gain +₹640/qtl at govt centres).\n"
                "• **Cotton (Medium Staple)**: MSP ₹7,121/qtl at Cotton Corporation of India (CCI) centres.\n"
                "• **Bengal Gram (Chana)**: MSP ₹5,440/qtl at NAFED centres.\n"
                "• **Sesame (Til)**: MSP ₹9,267/qtl (Highest MSP among oilseeds).\n\n"
                "👉 Check full comparison arbitrage in **Tab 6 (MSP vs Mandi)**!"
            )
        return {
            "status": "success",
            "query": query_text,
            "response": msg,
            "action": "view_msp",
            "url": "#msp-tracker"
        }

    # Fallback: General Guidance
    if lang == "te":
        fallback_msg = (
            f"🌾 మీ ప్రశ్న: *\"{query_text}\"*\n\n"
            "ఈ ప్రశ్నకు సంబంధించిన ప్రభుత్వ నిబంధనలను పరిశీలిస్తున్నాము. దయచేసి ఎడమవైపు గల మీ భూమి మరియు పంట వివరాలను నమోదు చేసి 'Check Eligible Schemes' బటన్ నొక్కండి, లేదా కింది ముఖ్య అంశాలను అడగండి:\n\n"
            "• **'పత్రాలు'** - కావలసిన ధ్రువపత్రాల వివరాలు\n"
            "• **'72 గంటల నష్టం'** - పంట బీమా నిబంధనలు\n"
            "• **'KCC రుణం'** - 4% వడ్డీ రాయితీ పంట రుణాలు\n"
            "• **'కౌలు హక్కులు'** - CCRC కార్డు నిబంధనలు"
        )
    else:
        fallback_msg = (
            f"🌾 Your query: *\"{query_text}\"*\n\n"
            "I am ready to help you with official agricultural rules. You can evaluate your farm by entering your land holding and crop on the left, or ask me directly about:\n\n"
            "• **'Documents'** — Required certificates & proofs for all schemes\n"
            "• **'72-Hour Claim'** — PMFBY localized crop loss emergency rules\n"
            "• **'KCC Loan'** — Scale of Finance & 4% interest subvention\n"
            "• **'Tenant CCRC'** — Legal protections for tenant cultivators\n"
            "• **'Water Subsidies'** — 18+ Drip, Sprinkler & Solar pump grants"
        )

    return {
        "status": "success",
        "query": query_text,
        "response": fallback_msg,
        "action": "info",
        "url": ""
    }




@app.post("/api/query_ai")
@app.post("/query_ai")
@app.get("/api/query_ai")
def query_ai_assistant(query: Optional[str] = None, language: str = "en", req: Optional[QueryAIRequest] = None):
    """Natural language AI query handler with deterministic agritech grounding."""
    effective_query = ""
    effective_lang = language or "en"
    if req and req.query:
        effective_query = req.query
        effective_lang = req.language or effective_lang
    elif query:
        effective_query = query
    
    if not effective_query:
        return {
            "status": "error",
            "message": "Query parameter is required",
            "response": "Please enter a valid farming question or scheme query."
        }
    
    return get_farmer_ai_response(effective_query, language=effective_lang)

@app.get("/climate_water_stress")
def get_climate_water_stress(district: str = "Warangal", state: Optional[str] = None, crop: str = "Paddy", water_source: str = "Borewell", lang: str = "en"):
    from utils.weather_api import get_live_weather, evaluate_water_stress, generate_multilingual_water_advisory
    weather = get_live_weather(district, state=state)
    assessment = evaluate_water_stress(weather, crop=crop, water_source=water_source)
    advisory_text = generate_multilingual_water_advisory(assessment, lang=lang)
    return {
        "weather": weather,
        "assessment": assessment,
        "advisory_text": advisory_text
    }


# Direct Route Aliases for Compatibility with tests, frontend, and offline suites
@app.get("/schemes")
def get_all_schemes():
    return load_schemes()

@app.get("/verify_name")
def get_verify_name(aadhaar_name: str, bank_name: str):
    clean_aadhaar = aadhaar_name.strip().lower().replace(".", " ")
    clean_bank = bank_name.strip().lower().replace(".", " ")
    ratio = int(fuzz.token_set_ratio(clean_aadhaar, clean_bank))
    status = "Exact Match" if ratio == 100 else ("Minor Variation" if ratio >= 80 else "Severe Mismatch")
    return {
        "aadhaar_name": aadhaar_name,
        "bank_name": bank_name,
        "similarity_score": ratio,
        "status": status,
        "requires_manual_verification": ratio < 100,
        "action_required": "None (Ready for DBT)" if ratio >= 80 else "Visit Bank branch or CSC with Aadhaar to update name."
    }

@app.get("/water_saving_schemes")
def get_water_saving_schemes_compat(state: Optional[str] = None):
    if not os.path.exists(WATER_SCHEMES_PATH):
        return []
    with open(WATER_SCHEMES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if state and state.lower() != "all":
        data = [s for s in data if "All States" in s.get("applicable_states", []) or state.lower() in [st.lower() for st in s.get("applicable_states", [])]]
    return data

@app.get("/low_water_crops")
def get_low_water_crops_compat(category: Optional[str] = None):
    if not os.path.exists(LOW_WATER_CROPS_PATH):
        return []
    with open(LOW_WATER_CROPS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if category and category.lower() != "all":
        data = [c for c in data if category.lower() in c.get("category", "").lower()]
    return data

@app.get("/disaster_relief")
@app.get("/api/disaster_relief")
def get_disaster_relief_info():
    disaster_path = os.path.join(str(PROJECT_ROOT), "data", "disaster_relief.json")
    if not os.path.exists(disaster_path):
        return {}
    with open(disaster_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/calculate_kcc")
def api_calculate_kcc_direct(req: KCCRequest):
    return calculate_kcc_eligibility(crop=req.crop, land_acres=req.land_acres, existing_kcc_debt=req.existing_debt)

@app.post("/generate_claim_sms")
def api_generate_claim_sms_direct(req: ClaimIntimationRequest):
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
def api_get_claims_direct():
    claims = get_all_claims()
    from utils.status_tracker import compute_claim_urgency
    for c in claims:
        c["urgency_meta"] = compute_claim_urgency(c)
    return claims

@app.post("/claims")
def api_add_claim_direct(req: ClaimEntryRequest):
    return add_claim_entry(
        farmer_name=req.farmer_name,
        phone=req.phone,
        scheme_name=req.scheme_name,
        reference_number=req.reference_number,
        status=req.status,
        notes=req.notes or ""
    )

@app.post("/feedback")
@app.post("/api/feedback")
def api_record_feedback_direct(req: FeedbackRequest):
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
@app.post("/api/escalate")
def api_escalate_grievance_direct(req: EscalationRequest):
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
@app.get("/api/documents")
def api_get_documents_direct(farmer_id: str = "DEMO_FARMER_1"):
    from utils.document_wallet import get_farmer_documents
    return get_farmer_documents(farmer_id)

class VoiceQueryRequest(BaseModel):
    query: str
    language: Optional[str] = "auto"

@app.post("/api/voice_assistant")
def api_voice_assistant(req: VoiceQueryRequest):
    """
    Multilingual voice assistant endpoint understanding and responding in any major Indian language.
    """
    from utils.voice_engine import get_voice_response
    return get_voice_response(query=req.query, lang_code=req.language or "auto")

@app.get("/api/documents/download/{doc_type}")
def api_download_sample_document(doc_type: str):
    """
    Serves downloadable official sample document copies for Aadhaar, Pahani, Passbook, and CCRC.
    """
    samples_dir = os.path.join(FRONTEND_DIR, "samples")
    doc_map = {
        "aadhaar": ("sample_aadhaar.svg", "Sample_Aadhaar_Card_Masked.svg"),
        "pahani": ("sample_pahani.svg", "Sample_Pahani_Land_Record_RoR1B.svg"),
        "land_record": ("sample_pahani.svg", "Sample_Pahani_Land_Record_RoR1B.svg"),
        "passbook": ("sample_passbook.svg", "Sample_Bank_Passbook_DBT_Active.svg"),
        "bank_passbook": ("sample_passbook.svg", "Sample_Bank_Passbook_DBT_Active.svg"),
        "ccrc": ("sample_ccrc.svg", "Sample_CCRC_Tenant_Card.svg"),
        "ccrc_tenancy": ("sample_ccrc.svg", "Sample_CCRC_Tenant_Card.svg")
    }
    key = doc_type.lower().strip()
    if key not in doc_map:
        raise HTTPException(status_code=404, detail=f"Document type '{doc_type}' not found.")
    file_name, download_name = doc_map[key]
    file_path = os.path.join(samples_dir, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample file not found on server")
    return FileResponse(
        path=file_path,
        filename=download_name,
        media_type="image/svg+xml",
        headers={"Content-Disposition": f'attachment; filename="{download_name}"'}
    )

class WeatherAdvisoryRequest(BaseModel):
    state: Optional[str] = "Telangana"
    district: Optional[str] = "Warangal"
    routine_crop: Optional[str] = "Paddy"
    irrigation_type: Optional[str] = "flood"
    acres: Optional[float] = 2.5
    farmer_category: Optional[str] = "small_marginal"

@app.post("/api/weather_advisory")
def api_weather_advisory(req: WeatherAdvisoryRequest):
    """
    Agro-climatic intelligence endpoint:
    Evaluates near-future weather dry spells, matches Drip Subsidies (Buy vs Rent),
    and calculates routine crop migration options.
    """
    from utils.agro_climate_advisory import compute_agro_climate_ecosystem
    return compute_agro_climate_ecosystem(
        state=req.state or "Telangana",
        district=req.district or "Warangal",
        routine_crop=req.routine_crop or "Paddy",
        irrigation_type=req.irrigation_type or "flood",
        acres=req.acres or 2.5,
        farmer_category=req.farmer_category or "small_marginal"
    )

@app.get("/api/weather_advisory")
def api_weather_advisory_get(
    state: str = "Telangana",
    district: Optional[str] = None,
    routine_crop: str = "Paddy",
    irrigation_type: str = "flood",
    acres: float = 2.5,
    farmer_category: str = "small_marginal"
):
    from utils.agro_climate_advisory import compute_agro_climate_ecosystem
    return compute_agro_climate_ecosystem(
        state=state,
        district=district,
        routine_crop=routine_crop,
        irrigation_type=irrigation_type,
        acres=acres,
        farmer_category=farmer_category
    )

@app.get("/api/weather_districts/{state}")
def api_get_weather_districts(state: str):
    from utils.agro_climate_advisory import DISTRICT_WEATHER_PROFILES
    districts = list(DISTRICT_WEATHER_PROFILES.get(state, {}).keys())
    if not districts:
        districts = ["District Capital / General"]
    return {"state": state, "districts": districts}

# Mount static files to serve the frontend portal
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
