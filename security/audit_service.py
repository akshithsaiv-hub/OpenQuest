"""
audit_service.py
================
Safeguard 8: Runtime Audit Logging Service.

Records immutable audit trails for profile reads, modifications, consent changes,
identity verifications, and intermediary accesses.
Guarantees that sensitive credentials, OTPs, and unnecessary PII are excluded from audit stores.
"""

import uuid
import logging
from datetime import datetime
from typing import Optional, Any

logger = logging.getLogger("DLP.AuditLogger")


def log_runtime_audit_event(
    action_type: str,
    target_resource: Optional[str] = None,
    record_id: Optional[str] = None,
    actor_id: Optional[str] = None,
    actor_role: Optional[str] = None,
    role: Optional[str] = None,
    target_table: Optional[str] = None,
    client_ip: Optional[str] = "127.0.0.1",
    db_path: Optional[Any] = None
) -> str:
    """
    Persist an audit event record to the audit_events table.
    Excludes sensitive payload bodies to prevent secondary data leaks.
    Accepts both (actor_role, target_resource) and (role, target_table) for caller convenience.
    """
    from person3.farmer_database import connect

    event_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat(timespec="seconds")
    effective_role = actor_role or role or "anonymous"
    effective_resource = target_resource or target_table or "general"

    try:
        with connect(db_path) as con:
            con.execute("""
                INSERT INTO audit_events (
                    event_id, actor_id, actor_role, action_type,
                    target_resource, record_id, client_ip, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_id,
                str(actor_id) if actor_id else None,
                str(effective_role),
                str(action_type),
                str(effective_resource),
                str(record_id) if record_id else None,
                str(client_ip) if client_ip else "127.0.0.1",
                created_at,
            ))
            con.commit()
    except Exception as e:
        logger.error("Failed to write audit event: %s", e)

    return event_id
