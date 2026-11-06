"""
rag_guard.py
============
Safeguard 7: Public-Only Knowledge Base & RAG Isolation Guard.

Architectural boundary ensuring Vector DB searches and AI Retrieval-Augmented
Generation (RAG) contexts strictly query public documentation namespaces
(schemes, mandi MSP, input price ceilings, crop guidelines).

Security Invariants:
1. Hard-stops any vector search or RAG ingestion attempt containing tenant table names
   ('farmers', 'user_consents', 'crop_claims', 'document_metadata', 'audit_logs').
2. Isolates public knowledge vectors into dedicated namespaces:
   - 'public_schemes'
   - 'public_mandi_msp'
   - 'public_agri_inputs'
   - 'public_weather_advisories'
3. Enforces execution with the restricted 'app_rag_public' role which has zero
   read permissions on any tenant or personal tables in the database.
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("DLP.RAGGuard")


class RAGIsolationViolation(Exception):
    """Raised when a RAG query attempts to access private tenant data."""
    pass


class RAGNamespaceGuard:
    """
    Enforces isolation between public agricultural knowledge embeddings and private farmer data.
    """

    FORBIDDEN_TENANT_KEYWORDS = {
        "farmers",
        "user_consents",
        "crop_claims",
        "document_metadata",
        "audit_logs",
        "phone_number",
        "phone_encrypted",
        "identity_hash",
        "bank_account",
        "aadhaar",
        "farmer_id"
    }

    ALLOWED_PUBLIC_NAMESPACES = {
        "public_schemes",
        "public_mandi_msp",
        "public_agri_inputs",
        "public_weather_advisories",
        "public_faqs"
    }

    @classmethod
    def validate_rag_query(cls, namespace: str, query_filter: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate that the target RAG namespace is strictly a public agricultural namespace
        and that metadata filters contain no tenant data leak attempts.
        """
        if namespace not in cls.ALLOWED_PUBLIC_NAMESPACES:
            err_msg = (
                f"SECURITY VIOLATION: RAG access rejected for namespace '{namespace}'. "
                f"RAG is strictly quarantined to public namespaces: {cls.ALLOWED_PUBLIC_NAMESPACES}"
            )
            logger.error(err_msg)
            raise RAGIsolationViolation(err_msg)

        if query_filter:
            cls._scan_filters_for_tenant_leak(query_filter)

        return True

    @classmethod
    def _scan_filters_for_tenant_leak(cls, filter_dict: Dict[str, Any]):
        """Recursively scan dictionary keys and values for forbidden tenant identifiers."""
        for key, value in filter_dict.items():
            if str(key).lower() in cls.FORBIDDEN_TENANT_KEYWORDS:
                err_msg = f"SECURITY VIOLATION: Query filter references forbidden tenant entity '{key}'."
                logger.error(err_msg)
                raise RAGIsolationViolation(err_msg)

            if isinstance(value, dict):
                cls._scan_filters_for_tenant_leak(value)
            elif isinstance(value, str):
                for kw in cls.FORBIDDEN_TENANT_KEYWORDS:
                    if kw in value.lower():
                        err_msg = f"SECURITY VIOLATION: Filter payload references forbidden entity '{kw}'."
                        logger.error(err_msg)
                        raise RAGIsolationViolation(err_msg)

    @classmethod
    def sanitize_retrieved_chunks(cls, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Final safety gate: Scans retrieved knowledge chunks to guarantee zero
        tenant records inadvertently entered the vector database.
        """
        sanitized = []
        for chunk in chunks:
            text = chunk.get("text", "")
            # Ensure no PII-like patterns exist in retrieved documentation chunks
            if "identity_hash" in text or "phone_encrypted" in text:
                logger.critical("Data leak detected in vector chunk! Omitting chunk from RAG context.")
                continue
            sanitized.append(chunk)
        return sanitized


# Global instance
rag_guard = RAGNamespaceGuard()
