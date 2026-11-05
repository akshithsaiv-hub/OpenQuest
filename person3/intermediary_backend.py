"""
intermediary_backend.py
=======================
CSC/FPO Intermediary Mode Backend (Task 6).
Generates actionable operational dashboards for CSC and FPO field staff.

Capabilities:
- Filters farmer records by CSC/FPO intermediary_id.
- Strictly excludes farmers who have withdrawn consent (consent_status = 0).
- Identifies farmers needing follow-up due to:
  * Missing documents for target schemes.
  * Potential bank name mismatches requiring manual review.
  * Upcoming or closing insurance claim-windows and application deadlines.
- Automatically sorts records by urgency (urgent claim windows first, then missing docs).
- Excludes unnecessary sensitive personal details.
"""

import json
from datetime import date
from typing import Any, Dict, List, Optional, Union
from person3.farmer_database import connect
from person3.document_checker import check_documents
from person3.reminder_engine import parse_date, load_schemes_from_file


def get_intermediary_farmers(
    scheme_data: Optional[List[Dict[str, Any]]] = None,
    today: Union[date, str] = date.today(),
    intermediary_id: Optional[str] = None,
    days_ahead: int = 30,
    db_path=None
) -> List[Dict[str, Any]]:
    """
    Query and return structured records for CSC/FPO staff assistance dashboard.

    Inputs:
    - scheme_data: List of government schemes from Person 1. If None, loaded from file.
    - today: Current date (date object or 'YYYY-MM-DD').
    - intermediary_id: Optional filter for a specific CSC/FPO staff identifier.
    - days_ahead: Horizon for upcoming deadlines (default: 30 days).
    - db_path: Optional custom SQLite path.

    Returns:
    List of actionable dictionaries ready for Person 2 UI display.
    """
    eval_date = parse_date(today)
    if not eval_date:
        raise ValueError(f"Invalid evaluation date: {today}")

    if scheme_data is None:
        scheme_data = load_schemes_from_file()

    results: List[Dict[str, Any]] = []

    # Fetch farmers with active consent only
    with connect(db_path) as con:
        if intermediary_id:
            query = """
                SELECT farmer_id, farmer_name, preferred_language,
                       intermediary_id, uploaded_documents, bank_account_name,
                       created_at
                FROM farmers
                WHERE consent_status = 1 AND intermediary_id = ?
                ORDER BY farmer_name ASC
            """
            rows = con.execute(query, (str(intermediary_id).strip(),)).fetchall()
        else:
            query = """
                SELECT farmer_id, farmer_name, preferred_language,
                       intermediary_id, uploaded_documents, bank_account_name,
                       created_at
                FROM farmers
                WHERE consent_status = 1
                ORDER BY farmer_name ASC
            """
            rows = con.execute(query).fetchall()

    for row in rows:
        raw_dict = dict(row)
        try:
            documents = json.loads(raw_dict.pop("uploaded_documents", "{}"))
        except Exception:
            documents = {}

        # Profile dict for checker
        profile = {
            "farmer_id": raw_dict["farmer_id"],
            "farmer_name": raw_dict["farmer_name"],
            "name": raw_dict["farmer_name"],
            "preferred_language": raw_dict["preferred_language"],
            "intermediary_id": raw_dict["intermediary_id"],
            "uploaded_documents": documents,
            "documents": documents,
            "bank_account_name": raw_dict["bank_account_name"],
            "bank_name": raw_dict["bank_account_name"],
        }

        for scheme in scheme_data:
            scheme_name = scheme.get("name") or scheme.get("scheme") or "Unnamed Scheme"
            readiness = check_documents(profile, scheme)

            # Dates
            deadline = parse_date(scheme.get("deadline"))
            claim_window = scheme.get("claim_window")
            claim_end = None
            if isinstance(claim_window, dict):
                claim_end = parse_date(claim_window.get("end"))
            elif isinstance(claim_window, str):
                claim_end = parse_date(claim_window)

            # Determine earliest due date
            due_date = claim_end or deadline
            days_left = (due_date - eval_date).days if due_date else None
            is_upcoming = (days_left is not None and 0 <= days_left <= days_ahead)

            has_missing_docs = len(readiness["missing"]) > 0
            has_mismatches = len(readiness["mismatches"]) > 0
            is_claim_window_urgent = (
                claim_end is not None and 0 <= (claim_end - eval_date).days <= 14
            )

            # Farmer requires assistance if paperwork is incomplete, name differs,
            # or deadline/claim-window is upcoming
            requires_assistance = has_missing_docs or has_mismatches or is_upcoming

            if requires_assistance:
                # Assign Priority Rank for sorting
                # 1 = Urgent Insurance Claim Window Closing
                # 2 = Missing Documents for Approaching Deadline
                # 3 = Name Mismatch Requiring Verification
                # 4 = General Upcoming Deadline
                if is_claim_window_urgent:
                    priority_rank = 1
                    priority_label = "CRITICAL: Insurance Claim Window Closing"
                elif has_missing_docs and (days_left is not None and days_left <= 14):
                    priority_rank = 2
                    priority_label = "HIGH: Missing Docs on Approaching Deadline"
                elif has_mismatches:
                    priority_rank = 3
                    priority_label = "ATTENTION: Name Mismatch Review"
                elif has_missing_docs:
                    priority_rank = 4
                    priority_label = "MODERATE: Document Collection Required"
                else:
                    priority_rank = 5
                    priority_label = "INFO: Approaching Deadline"

                # Format human readable mismatch warning if any
                mismatch_warnings = [
                    m.get("message", "Name discrepancy detected.")
                    for m in readiness["mismatches"]
                ]
                name_warning_str = "; ".join(mismatch_warnings) if mismatch_warnings else ""

                results.append({
                    "farmer_id": profile["farmer_id"],
                    "farmer_name": profile["farmer_name"],
                    "intermediary_id": profile["intermediary_id"],
                    "scheme": scheme_name,
                    "missing_documents": readiness["missing"],
                    "mismatches": readiness["mismatches"],
                    "name_mismatch_warning": name_warning_str,
                    "upcoming_claim_deadlines": claim_end.isoformat() if claim_end else None,
                    "scheme_deadline": deadline.isoformat() if deadline else None,
                    "remaining_days": days_left,
                    "days_left": days_left,
                    "priority_rank": priority_rank,
                    "priority_label": priority_label,
                    "requires_assistance": True,
                })

    # Sort results so highest priority (lowest rank) and fewest days remaining appear first
    results.sort(key=lambda item: (
        item["priority_rank"],
        item["remaining_days"] if item["remaining_days"] is not None else 9999
    ))

    return results
