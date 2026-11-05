"""
document_checker.py
===================
Document Readiness Checker (Task 4) and Name Mismatch Detection (Task 5).

Capabilities:
- Compares scheme required documents against farmer profile documents.
- Uses RapidFuzz (with clean fallback) for fuzzy name matching between
  farmer profile name and bank account name.
- Highlights potential mismatches without accusing users of fraud or altering data.
- Explicitly distinguishes document completeness from statutory scheme eligibility.
"""

import difflib
import re
from typing import Any, Dict, List, Optional, Tuple

# Try to import RapidFuzz for fuzzy string similarity; fallback to difflib
try:
    from rapidfuzz.fuzz import ratio as rapidfuzz_ratio
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False


def normalize_name(value: Optional[str]) -> str:
    """
    Standardize name string:
    - strip leading/trailing whitespace
    - lowercase
    - collapse multiple interior spaces
    """
    if not value:
        return ""
    # Remove any non-alphanumeric noise if appropriate, but keep standard spaces
    cleaned = re.sub(r"[^\w\s]", "", str(value), flags=re.UNICODE)
    return " ".join(cleaned.lower().split())


def check_name_match(
    farmer_name: Optional[str],
    bank_account_name: Optional[str],
    mismatch_threshold: float = 85.0
) -> Dict[str, Any]:
    """
    Compare farmer name and bank account name.
    
    Returns structured analysis:
    {
        "match_status": "matched" | "possible_mismatch" | "mismatch" | "missing_name",
        "similarity_score": float,
        "requires_manual_verification": bool,
        "warning_message": str,
        "method_used": "rapidfuzz" | "fallback"
    }

    Ethical Guideline:
    A mismatch is NOT proof of fraud; it simply flags the record for manual
    verification by CSC/FPO staff to prevent subsidy transfer failures.
    """
    norm_farmer = normalize_name(farmer_name)
    norm_bank = normalize_name(bank_account_name)

    if not norm_farmer or not norm_bank:
        return {
            "match_status": "missing_name",
            "similarity_score": 0.0,
            "requires_manual_verification": True,
            "warning_message": (
                "Bank account name or farmer profile name is missing. "
                "Manual review required."
            ),
            "method_used": "none"
        }

    # Perfect match after normalization
    if norm_farmer == norm_bank:
        return {
            "match_status": "matched",
            "similarity_score": 100.0,
            "requires_manual_verification": False,
            "warning_message": "",
            "method_used": "exact_normalization"
        }

    # Calculate similarity score
    if RAPIDFUZZ_AVAILABLE:
        score = float(rapidfuzz_ratio(norm_farmer, norm_bank))
        method = "rapidfuzz"
    else:
        # Standard library difflib fallback
        matcher = difflib.SequenceMatcher(None, norm_farmer, norm_bank)
        score = round(matcher.ratio() * 100.0, 1)
        method = "fallback_difflib"

    # Match evaluation
    if score >= mismatch_threshold:
        # High similarity but minor discrepancy (e.g. "Ravi Kumar" vs "Ravi Kumer")
        return {
            "match_status": "possible_mismatch",
            "similarity_score": round(score, 1),
            "requires_manual_verification": True,
            "warning_message": (
                f"Minor spelling variation detected between farmer name ('{farmer_name}') "
                f"and bank name ('{bank_account_name}') with similarity {round(score, 1)}%. "
                "Manual verification recommended."
            ),
            "method_used": method
        }
    else:
        # Substantial difference
        return {
            "match_status": "mismatch",
            "similarity_score": round(score, 1),
            "requires_manual_verification": True,
            "warning_message": (
                f"Potential mismatch between farmer name ('{farmer_name}') and "
                f"bank name ('{bank_account_name}') with similarity {round(score, 1)}%. "
                "Please verify bank passbook before submitting scheme application."
            ),
            "method_used": method
        }


def _normalize_doc_title(title: str) -> str:
    """Normalize document title for case and space-insensitive matching."""
    return "".join(re.sub(r"[^\w]", "", title.lower()))


def check_documents(profile: Dict[str, Any], scheme: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify document readiness for a given farmer profile and scheme.
    
    Inputs:
    - profile: dict containing 'uploaded_documents' / 'documents',
      'farmer_name' / 'name', and 'bank_account_name' / 'bank_name'.
    - scheme: dict containing 'documents_required' or 'docs',
      and optional 'name_match_required'.

    Output:
    {
        "ready": bool,
        "missing": List[str],
        "mismatches": List[dict]
    }

    Note:
    Document readiness only indicates whether prerequisite paperwork is collected.
    Statutory scheme eligibility is determined solely by Person 1's engine.
    """
    # 1. Resolve required documents from Person 1's scheme specification
    raw_required = scheme.get("documents_required")
    if raw_required is None:
        raw_required = scheme.get("docs", [])

    required_list = []
    for item in raw_required:
        if isinstance(item, dict):
            name = item.get("name") or item.get("doc_name")
            if name:
                required_list.append(name)
        elif isinstance(item, str):
            required_list.append(item)

    # 2. Resolve documents currently available in farmer's profile
    available_docs = profile.get("uploaded_documents")
    if available_docs is None:
        available_docs = profile.get("documents", {})

    available_map = {}
    if isinstance(available_docs, dict):
        for k, v in available_docs.items():
            if v:  # Boolean True, or non-empty string/status
                available_map[_normalize_doc_title(k)] = k
    elif isinstance(available_docs, list):
        for k in available_docs:
            available_map[_normalize_doc_title(str(k))] = str(k)

    # 3. Identify missing documents
    missing = []
    for req in required_list:
        norm_req = _normalize_doc_title(req)
        if norm_req not in available_map:
            missing.append(req)

    # 4. Check for name mismatches if required by the scheme
    mismatches = []
    name_check_needed = scheme.get("name_match_required", True)
    if name_check_needed:
        farmer_name = profile.get("farmer_name") or profile.get("name")
        bank_name = profile.get("bank_account_name") or profile.get("bank_name")

        if bank_name:
            match_res = check_name_match(farmer_name, bank_name)
            if match_res["requires_manual_verification"]:
                mismatches.append({
                    "field": "farmer_name_vs_bank_name",
                    "match_status": match_res["match_status"],
                    "similarity_score": match_res["similarity_score"],
                    "requires_manual_verification": True,
                    "message": match_res["warning_message"]
                })

    is_ready = (len(missing) == 0 and len(mismatches) == 0)

    return {
        "ready": is_ready,
        "missing": missing,
        "mismatches": mismatches
    }
