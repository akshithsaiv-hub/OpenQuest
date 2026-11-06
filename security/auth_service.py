"""
auth_service.py
===============
Safeguard 4: Authentication, Authorization, and Session Scoping.

Provides role-based access control (RBAC) and cryptographic session token
issuance for farmers, intermediaries, and government officers.
Ensures that all account-specific queries strictly derive identities from
the verified token rather than untrusted request bodies or URL parameters.
"""

import os
import time
import json
import base64
import hmac
import hashlib
import secrets
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, Header, Depends, status

# Load signing secret key; in development generates a secure ephemeral key if not set
_SECRET = os.getenv("AUTH_SECRET_KEY")
if not _SECRET:
    _SECRET = secrets.token_hex(32)


class AuthContext:
    """Holds verified identity and role claims for an authenticated session."""
    def __init__(self, subject_id: str, role: str, phone: Optional[str] = None):
        self.subject_id = str(subject_id).strip()
        self.role = str(role).strip().lower()
        self.phone = phone

    def __getitem__(self, item: str):
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

    def get(self, key: str, default=None):
        return getattr(self, key, default)

    def is_farmer(self) -> bool:
        return self.role == "farmer"

    def is_intermediary(self) -> bool:
        return self.role == "intermediary"

    def is_officer(self) -> bool:
        return self.role == "officer"


def create_session_token(subject_id: str, role: str, phone: Optional[str] = None, expires_in: int = 86400) -> str:
    """
    Generate an HMAC-SHA256 signed session token.
    Token format: base64(payload).base64(signature)
    """
    now = int(time.time())
    payload = {
        "sub": str(subject_id),
        "role": str(role).lower(),
        "phone": phone,
        "iat": now,
        "exp": now + expires_in,
    }
    payload_bytes = json.dumps(payload, separators=(',', ':')).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode("utf-8").rstrip("=")
    
    sig = hmac.new(_SECRET.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode("utf-8").rstrip("=")
    
    return f"{payload_b64}.{sig_b64}"


def verify_session_token(token: str) -> AuthContext:
    """
    Verify signature and expiration of an HMAC-SHA256 token.
    Raises HTTPException(401) upon invalid signature or expiration.
    """
    if not token or "." not in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED: Missing or malformed authorization token."
        )

    parts = token.split(".")
    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED: Invalid token structure."
        )

    payload_b64, sig_b64 = parts
    expected_sig = hmac.new(_SECRET.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).digest()
    expected_b64 = base64.urlsafe_b64encode(expected_sig).decode("utf-8").rstrip("=")

    if not secrets.compare_digest(sig_b64, expected_b64):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED: Invalid token signature."
        )

    # Decode payload
    padding = 4 - (len(payload_b64) % 4)
    if padding != 4:
        payload_b64 += "=" * padding

    try:
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED: Could not decode token payload."
        )

    if int(time.time()) > payload.get("exp", 0):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED: Session token has expired."
        )

    return AuthContext(
        subject_id=payload["sub"],
        role=payload["role"],
        phone=payload.get("phone")
    )


def get_token_claims(token: str) -> Dict[str, Any]:
    """Extract claims dictionary from token."""
    auth_ctx = verify_session_token(token)
    return {"sub": auth_ctx.subject_id, "role": auth_ctx.role, "phone": auth_ctx.phone}


# FastAPI Dependencies
def get_current_user(authorization: Optional[str] = Header(None)) -> AuthContext:
    """
    Extracts Bearer token from Authorization header and verifies claims.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED: Authorization header missing or malformed."
        )
    raw_token = authorization.split("Bearer ")[1].strip()
    return verify_session_token(raw_token)


def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[AuthContext]:
    """
    Non-blocking token extractor: returns AuthContext if valid Bearer token provided, None otherwise.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        raw_token = authorization.split("Bearer ")[1].strip()
        return verify_session_token(raw_token)
    except HTTPException:
        return None


def require_role(allowed_roles: List[str]):
    """
    Factory dependency checking that user has one of the allowed roles.
    """
    def _role_checker(user: AuthContext = Depends(get_current_user)) -> AuthContext:
        if user.role not in [r.lower() for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"FORBIDDEN: Access requires one of roles {allowed_roles}. Current role: '{user.role}'."
            )
        return user
    return _role_checker
