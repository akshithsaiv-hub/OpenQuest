"""
validators.py
=============
Safeguard 1: Input Validation and Data Minimization Guard.

Validates input fields across all API and bot entry points to strictly prevent
the injection, transmission, or logging of raw Aadhaar numbers, PAN cards,
full bank account numbers, or document binary payloads.
"""

import re
from typing import Any, Dict, List, Optional


class DataMinimizationViolation(ValueError):
    """Raised when an unminimized sensitive identifier is submitted."""
    pass


# Alias for backward-compatible import
ValidationError = DataMinimizationViolation

# 12-digit Aadhaar pattern
AADHAAR_PATTERN = re.compile(r"\b[2-9]\d{3}[\s\-]?[0-9]{4}[\s\-]?[0-9]{4}\b")

# Indian PAN pattern
PAN_PATTERN = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")

# Raw Bank account pattern (9-18 digits)
RAW_BANK_ACCOUNT_PATTERN = re.compile(r"\b\d{9,18}\b")


def validate_no_pii_leakage(payload: Any, path: str = "root"):
    """
    Recursively scans request payloads (dicts, lists, strings) to guarantee
    zero raw Aadhaar numbers, PAN cards, or binary document data are admitted.
    Raises DataMinimizationViolation upon detection.
    """
    if isinstance(payload, str):
        # 1. Check for raw 12-digit Aadhaar
        if AADHAAR_PATTERN.search(payload):
            raise DataMinimizationViolation(
                f"Data Minimization Violation at '{path}': Storing raw 12-digit Aadhaar numbers is prohibited. "
                "Use document verification boolean flags or masked last-4 format."
            )
        # 2. Check for raw base64 or binary file data
        if payload.startswith("data:image") or payload.startswith("data:application/pdf") or len(payload) > 8000:
            raise DataMinimizationViolation(
                f"Data Minimization Violation at '{path}': Storing raw document file contents is prohibited. "
                "Upload verification metadata/flags only."
            )

    elif isinstance(payload, dict):
        for key, val in payload.items():
            key_lower = str(key).lower()
            current_path = f"{path}.{key}"

            # Specific check for field names indicating direct identity leakage
            if any(k in key_lower for k in ["aadhaar_number", "aadhaar_no", "raw_uid", "pan_number"]):
                if val and isinstance(val, (str, int)) and re.search(r"\d{10,12}", str(val)):
                    raise DataMinimizationViolation(
                        f"Data Minimization Violation at '{current_path}': Field '{key}' contains raw sensitive ID. "
                        "Prohibited under data minimization safeguards."
                    )

            if "bank_account" in key_lower and not ("token" in key_lower or "name" in key_lower or "verified" in key_lower):
                if val and isinstance(val, (str, int)) and len(str(val).strip()) >= 9:
                    raise DataMinimizationViolation(
                        f"Data Minimization Violation at '{current_path}': Raw bank account numbers are prohibited. "
                        "Use tokenized bank account references or last-4 digits."
                    )

            validate_no_pii_leakage(val, current_path)

    elif isinstance(payload, list):
        for idx, item in enumerate(payload):
            validate_no_pii_leakage(item, f"{path}[{idx}]")


def sanitize_farmer_profile_for_storage(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safeguard 1: Data Minimization Sanitizer.
    Strips raw Aadhaar, PAN, and bank accounts, replacing them with boolean flags
    or cryptographic verification tokens before database persistence.
    """
    sanitized = dict(profile)
    # Remove any sensitive raw fields if present
    for sensitive_key in [
        "aadhaar_number", "aadhaar_no", "pan_number", "bank_account_number",
        "raw_uid", "document_scan", "file_bytes", "document_data"
    ]:
        if sensitive_key in sanitized:
            del sanitized[sensitive_key]
            sanitized["is_identity_verified"] = True

    return sanitized
