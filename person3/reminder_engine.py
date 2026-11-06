"""
reminder_engine.py
==================
Smart Reminder Engine (Task 3).
Calculates and prioritizes upcoming deadline reminders for farmers.

Key Rules:
- Excludes farmers who have withdrawn consent (consent_status = 0).
- Prioritises crop insurance claim-windows over general scheme application deadlines.
- Configurable notification horizon (default: 7 days before deadline).
- Prevents duplicate alerts for the same event.
- Flags and handles expired deadlines (past due date) without emitting false upcoming alerts.
- Sources scheme dates strictly from Person 1's scheme data/JSON.
"""

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from person3.farmer_database import connect

DEFAULT_SCHEMES_FILE = Path("data") / "schemes.json"


def parse_date(value: Any) -> Optional[date]:
    """
    Safely parse date from string (YYYY-MM-DD or ISO format) or date object.
    Returns None if missing or unparseable.
    """
    if not value:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    try:
        clean_str = str(value).strip()[:10]
        return date.fromisoformat(clean_str)
    except Exception:
        return None


def is_deadline_expired(deadline: Any, today: Union[date, str]) -> bool:
    """
    Check if a given deadline date is already in the past.
    """
    parsed_dl = parse_date(deadline)
    parsed_today = parse_date(today)
    if not parsed_dl or not parsed_today:
        return False
    return parsed_dl < parsed_today


def load_schemes_from_file(file_path: Optional[Union[str, Path]] = None) -> List[Dict[str, Any]]:
    """
    Load scheme knowledge base from Person 1's JSON file.
    Checks data/schemes.json or root schemes.json.
    """
    target = Path(file_path) if file_path else DEFAULT_SCHEMES_FILE
    if not target.exists() and Path("schemes.json").exists():
        target = Path("schemes.json")
    if target.exists():
        with open(target, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_due_alerts(
    today: Union[date, str],
    scheme_data: Optional[List[Dict[str, Any]]] = None,
    days_before: int = 7,
    db_path=None,
    include_expired: bool = False
) -> List[Dict[str, Any]]:
    """
    Identify and return due alerts for farmers with active consent.

    Inputs:
    - today: date object or 'YYYY-MM-DD' string representing current evaluation date.
    - scheme_data: List of schemes from Person 1. If None, loaded from schemes.json.
    - days_before: Notification window (default: 7 days before deadline).
    - db_path: Optional custom SQLite database path.
    - include_expired: Whether to include expired deadlines flagged with 'deadline_expired'.

    Returns structured alerts:
    [
        {
            "farmer_id": "...",
            "farmer_name": "...",
            "scheme": "...",
            "days_left": 3,
            "message_key": "claim_window_closing" | "scheme_deadline_approaching",
            "due_date": "YYYY-MM-DD",
            "event_type": "insurance_claim_window" | "scheme_deadline",
            "priority": 1 (Highest) or 2
        }
    ]
    """
    eval_date = parse_date(today)
    if not eval_date:
        raise ValueError(f"Invalid date for 'today': {today}")

    if scheme_data is None:
        scheme_data = load_schemes_from_file()

    alerts: List[Dict[str, Any]] = []
    seen_farmer_events = set()

    # Query only farmers with active consent
    with connect(db_path) as con:
        rows = con.execute(
            "SELECT farmer_id, farmer_name, preferred_language FROM farmers WHERE consent_status = 1 AND is_deleted = 0"
        ).fetchall()

    for farmer in rows:
        fid = farmer["farmer_id"]
        fname = farmer["farmer_name"]
        lang = farmer["preferred_language"]

        for scheme in scheme_data:
            scheme_name = scheme.get("name") or scheme.get("scheme") or "Unnamed Scheme"
            
            # Check for Crop Insurance Claim Window
            claim_window = scheme.get("claim_window")
            window_end = None
            if isinstance(claim_window, dict):
                window_end = parse_date(claim_window.get("end"))
            elif isinstance(claim_window, str):
                window_end = parse_date(claim_window)

            # Check for General Scheme Deadline
            deadline = parse_date(scheme.get("deadline"))

            alert_emitted_for_scheme = False

            # Priority 1: Crop Insurance Claim Window (time-critical)
            if window_end:
                days_left = (window_end - eval_date).days
                event_key = (fid, scheme_name, "claim_window")

                if 0 <= days_left <= days_before:
                    if event_key not in seen_farmer_events:
                        seen_farmer_events.add(event_key)
                        alerts.append({
                            "farmer_id": fid,
                            "farmer_name": fname,
                            "preferred_language": lang,
                            "scheme": scheme_name,
                            "days_left": days_left,
                            "message_key": "claim_window_closing",
                            "due_date": window_end.isoformat(),
                            "event_type": "insurance_claim_window",
                            "priority": 1,
                        })
                        alert_emitted_for_scheme = True
                elif days_left < 0 and include_expired:
                    if event_key not in seen_farmer_events:
                        seen_farmer_events.add(event_key)
                        alerts.append({
                            "farmer_id": fid,
                            "farmer_name": fname,
                            "preferred_language": lang,
                            "scheme": scheme_name,
                            "days_left": days_left,
                            "message_key": "claim_window_expired",
                            "due_date": window_end.isoformat(),
                            "event_type": "insurance_claim_window",
                            "priority": 3,
                        })

            # Priority 2: General Scheme Application Deadline
            # Avoid duplicate alert if urgent claim-window alert was already scheduled
            if deadline and not alert_emitted_for_scheme:
                days_left = (deadline - eval_date).days
                event_key = (fid, scheme_name, "scheme_deadline")

                if 0 <= days_left <= days_before:
                    if event_key not in seen_farmer_events:
                        seen_farmer_events.add(event_key)
                        alerts.append({
                            "farmer_id": fid,
                            "farmer_name": fname,
                            "preferred_language": lang,
                            "scheme": scheme_name,
                            "days_left": days_left,
                            "message_key": "scheme_deadline_approaching",
                            "due_date": deadline.isoformat(),
                            "event_type": "scheme_deadline",
                            "priority": 2,
                        })
                elif days_left < 0 and include_expired:
                    if event_key not in seen_farmer_events:
                        seen_farmer_events.add(event_key)
                        alerts.append({
                            "farmer_id": fid,
                            "farmer_name": fname,
                            "preferred_language": lang,
                            "scheme": scheme_name,
                            "days_left": days_left,
                            "message_key": "deadline_expired",
                            "due_date": deadline.isoformat(),
                            "event_type": "scheme_deadline",
                            "priority": 3,
                        })

    # Sort alerts: Claim windows first (priority 1), then fewest days_left first
    return sorted(alerts, key=lambda a: (a["priority"], a["days_left"]))


def get_expired_deadlines(
    today: Union[date, str],
    scheme_data: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Inspect scheme knowledge base and identify schemes or claim windows
    that have already expired relative to 'today'.
    """
    eval_date = parse_date(today)
    if not eval_date:
        raise ValueError(f"Invalid date: {today}")

    if scheme_data is None:
        scheme_data = load_schemes_from_file()

    expired = []
    for scheme in scheme_data:
        scheme_name = scheme.get("name") or scheme.get("scheme") or "Unnamed Scheme"
        claim_window = scheme.get("claim_window")
        window_end = None
        if isinstance(claim_window, dict):
            window_end = parse_date(claim_window.get("end"))
        elif isinstance(claim_window, str):
            window_end = parse_date(claim_window)

        deadline = parse_date(scheme.get("deadline"))

        if window_end and window_end < eval_date:
            expired.append({
                "scheme": scheme_name,
                "event": "claim_window",
                "due_date": window_end.isoformat(),
                "days_expired": (eval_date - window_end).days
            })
        if deadline and deadline < eval_date:
            expired.append({
                "scheme": scheme_name,
                "event": "scheme_deadline",
                "due_date": deadline.isoformat(),
                "days_expired": (eval_date - deadline).days
            })

    return expired
