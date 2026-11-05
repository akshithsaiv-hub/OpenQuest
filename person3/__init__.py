"""
Person 3 Backend Package - Farmer Assistance System
===================================================
Exports core functions for Farmer Profile Management, Consent,
Reminders, Document Readiness, Name Matching, and Intermediary Support.
"""

from person3.farmer_database import (
    init_db,
    connect,
    get_db_path,
)
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

__all__ = [
    "init_db",
    "connect",
    "get_db_path",
    "save_profile",
    "get_profile",
    "update_profile",
    "search_farmer",
    "list_all_farmers",
    "validate_consent",
    "get_consent_terms",
    "withdraw_consent",
    "grant_consent",
    "is_consent_active",
    "normalize_name",
    "check_name_match",
    "check_documents",
    "parse_date",
    "is_deadline_expired",
    "load_schemes_from_file",
    "get_due_alerts",
    "get_expired_deadlines",
    "get_intermediary_farmers",
]
