"""
person3_backend.py
==================
Main entrypoint and integration hub for Person 3 Backend Services.
Farmer Assistance System - Hackathon Edition.

Provides direct access to all Person 3 features:
1. Farmer Profile Management (SQLite)
2. Consent Management & Withdrawal
3. Smart Reminder Engine (Insurance Claim Window Prioritisation)
4. Document Readiness Checker
5. Aadhaar-Bank Account Name Mismatch Detection (RapidFuzz / fallback)
6. CSC/FPO Intermediary Mode Backend

Usage:
    python person3_backend.py
"""

import sys
from pathlib import Path
from datetime import date, datetime

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from person3.farmer_database import connect, init_db, get_db_path
from person3.farmer_profiles import (
    save_profile,
    get_profile,
    update_profile,
    search_farmer,
    list_all_farmers,
)
from person3.consent_manager import (
    validate_consent,
    get_consent_terms,
    withdraw_consent,
    grant_consent,
    is_consent_active,
)
from person3.document_checker import (
    normalize_name,
    check_name_match,
    check_documents,
)
from person3.reminder_engine import (
    parse_date,
    is_deadline_expired,
    load_schemes_from_file,
    get_due_alerts,
    get_expired_deadlines,
)
from person3.intermediary_backend import (
    get_intermediary_farmers,
)

# Aliases for 100% backward compatibility with legacy scripts
_normalise_name = normalize_name
_parse_date = parse_date


def _name_match(name_a, name_b):
    """Legacy helper returning (matched_bool, score_float)."""
    res = check_name_match(name_a, name_b)
    return (res["match_status"] == "matched", res["similarity_score"])


if __name__ == "__main__":
    print("=" * 70)
    print("FARMER ASSISTANCE SYSTEM - PERSON 3 BACKEND DEMO")
    print("=" * 70)

    # 1. Initialize SQLite Database
    db_file = init_db()
    print(f"\n[1] SQLite Database initialized at: {db_file}")

    # 2. Register Fictional Demo Farmer (Task 1 & Task 2)
    demo_farmer = {
        "farmer_id": "DEMO_F001",
        "farmer_name": "Ravi Kumar",
        "phone_number": "9876543210",
        "preferred_language": "Telugu",
        "intermediary_id": "CSC_WARANGAL_01",
        "consent_status": True,
        "uploaded_documents": {
            "Aadhaar": True,
            "Bank Passbook": False,
            "Land Records": True,
        },
        "bank_account_name": "Ravi Kumer",  # Slight spelling variation
    }

    print("\n[2] Registering farmer with consent...")
    try:
        # If already exists from previous run, update instead
        existing = get_profile("DEMO_F001")
        if existing:
            profile = update_profile("DEMO_F001", demo_farmer)
            print("   -> Existing demo profile updated.")
        else:
            profile = save_profile(demo_farmer)
            print(f"   -> Successfully registered: {profile['farmer_name']} (ID: {profile['farmer_id']})")
    except Exception as e:
        print(f"   -> Registration error: {e}")
        profile = get_profile("DEMO_F001")

    # 3. Test Name Mismatch Detection (Task 5)
    print("\n[3] Testing Name Mismatch Detection between Profile & Bank Account:")
    name_check = check_name_match(profile["farmer_name"], profile["bank_account_name"])
    print(f"   - Farmer Name: {profile['farmer_name']}")
    print(f"   - Bank Name:   {profile['bank_account_name']}")
    print(f"   - Match Status: {name_check['match_status']}")
    print(f"   - Similarity:   {name_check['similarity_score']}%")
    print(f"   - Requires Manual Review: {name_check['requires_manual_verification']}")
    print(f"   - Warning: {name_check['warning_message']}")

    # 4. Test Document Readiness Checker (Task 4)
    print("\n[4] Testing Document Readiness Checker:")
    schemes = load_schemes_from_file()
    pmfby_scheme = next((s for s in schemes if "PMFBY" in s.get("scheme_id", "")), schemes[0])
    doc_status = check_documents(profile, pmfby_scheme)
    print(f"   - Scheme: {pmfby_scheme['name']}")
    print(f"   - Documents Ready: {doc_status['ready']}")
    print(f"   - Missing Documents: {doc_status['missing']}")
    print(f"   - Mismatches Flagged: {len(doc_status['mismatches'])}")

    # 5. Test Smart Reminder Engine with Claim Window Prioritisation (Task 3)
    # Today's reference date set to 2026-11-05
    ref_today = date(2026, 11, 5)
    print(f"\n[5] Calculating Due Alerts for date {ref_today}:")
    alerts = get_due_alerts(ref_today, schemes, days_before=7)
    for alert in alerts:
        print(f"   * Priority {alert['priority']} Alert: Farmer {alert['farmer_id']} | "
              f"Scheme: {alert['scheme']} | "
              f"Days Left: {alert['days_left']} | "
              f"Message Key: '{alert['message_key']}'")

    # 6. Test CSC/FPO Intermediary Mode (Task 6)
    print("\n[6] Intermediary Dashboard Query (for CSC_WARANGAL_01):")
    intermediary_list = get_intermediary_farmers(
        schemes, today=ref_today, intermediary_id="CSC_WARANGAL_01"
    )
    for item in intermediary_list:
        print(f"   - Farmer: {item['farmer_name']} ({item['farmer_id']})")
        print(f"     Priority: {item['priority_label']}")
        print(f"     Scheme: {item['scheme']}")
        print(f"     Missing Docs: {item['missing_documents']}")
        print(f"     Days Remaining: {item['remaining_days']}")
        if item['name_mismatch_warning']:
            print(f"     Warning: {item['name_mismatch_warning']}")

    print("\n" + "=" * 70)
    print("DEMO RUN COMPLETED SUCCESSFULLY.")
    print("=" * 70)
