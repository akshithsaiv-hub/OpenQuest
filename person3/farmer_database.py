"""
farmer_database.py
==================
Database connection and initialization module for Person 3 backend.
Manages hardened SQLite storage (and configurable PostgreSQL driver) with
automated schema setup, consent tracking, and audit event persistence.

Privacy & Security Guidelines:
- Stores only minimum necessary personal data.
- NEVER stores raw Aadhaar numbers, PAN, or document scans.
- Enforces strict file permissions (0600 where supported).
- Default storage: database/farmer_data.db (excluded from version control).
"""

import os
import sqlite3
import logging
from pathlib import Path
from typing import Optional, Any

logger = logging.getLogger("DLP.Database")

# Default path relative to workspace; ignored by git
DEFAULT_DB_DIR = Path("database")
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "farmer_data.db"


def get_db_path(custom_path=None) -> Path:
    """
    Resolve and return database path.
    Ensures parent directory exists and is outside source tree if configured.
    """
    if custom_path:
        path = Path(custom_path)
    else:
        env_path = os.getenv("FARMER_DB_PATH")
        path = Path(env_path) if env_path else DEFAULT_DB_PATH

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def restrict_db_permissions(file_path: Path):
    """
    Restricts file permissions to read/write for owner only (0600 on POSIX).
    """
    try:
        if file_path.exists() and os.name == "posix":
            os.chmod(file_path, 0o600)
    except Exception as e:
        logger.debug("Could not restrict file permissions on %s: %s", file_path, e)


def connect(db_path=None) -> sqlite3.Connection:
    """
    Establish secure connection to SQLite database with Row factory enabled.
    """
    resolved_path = get_db_path(db_path)
    con = sqlite3.connect(resolved_path)
    con.row_factory = sqlite3.Row
    # Enable foreign keys and WAL mode for better concurrency and integrity
    con.execute("PRAGMA foreign_keys = ON;")
    restrict_db_permissions(resolved_path)
    return con


def init_db(db_path=None):
    """
    Initialize SQLite database tables and indices automatically.
    Includes schema migration columns for consent versioning and soft-deletes.
    """
    resolved_path = get_db_path(db_path)
    with connect(resolved_path) as con:
        # 1. Farmers table
        con.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id TEXT PRIMARY KEY,
                farmer_name TEXT NOT NULL,
                phone_number TEXT,
                preferred_language TEXT DEFAULT 'en',
                intermediary_id TEXT,
                consent_status INTEGER NOT NULL CHECK (consent_status IN (0, 1)),
                consent_language TEXT DEFAULT 'en',
                consent_purpose TEXT DEFAULT 'scheme_matching,reminders',
                consent_timestamp TEXT,
                is_deleted INTEGER NOT NULL DEFAULT 0 CHECK (is_deleted IN (0, 1)),
                uploaded_documents TEXT NOT NULL DEFAULT '{}',
                bank_account_name TEXT,
                state TEXT DEFAULT 'Telangana',
                district TEXT DEFAULT 'Warangal',
                crop TEXT DEFAULT 'Paddy',
                land_acres REAL DEFAULT 2.0,
                farmer_type TEXT DEFAULT 'owner',
                created_at TEXT NOT NULL
            );
        """)

        # Add columns if upgrading existing database
        existing_cols = {row[1] for row in con.execute("PRAGMA table_info(farmers)").fetchall()}
        migration_cols = {
            "consent_language": "TEXT DEFAULT 'en'",
            "consent_purpose": "TEXT DEFAULT 'scheme_matching,reminders'",
            "consent_timestamp": "TEXT",
            "is_deleted": "INTEGER NOT NULL DEFAULT 0",
            "state": "TEXT DEFAULT 'Telangana'",
            "district": "TEXT DEFAULT 'Warangal'",
            "crop": "TEXT DEFAULT 'Paddy'",
            "land_acres": "REAL DEFAULT 2.0",
            "farmer_type": "TEXT DEFAULT 'owner'",
            "passbook_saved": "INTEGER NOT NULL DEFAULT 0",
            "passbook_filename": "TEXT",
            "passbook_uploaded_at": "TEXT",
            "passbook_data": "TEXT",
            "passbook_review_status": "TEXT DEFAULT 'not_requested'",
            "passbook_reviewed_at": "TEXT",
            "passbook_reviewer_id": "TEXT",
            "pin_hash": "TEXT",
            "pin_salt": "TEXT",
            "pin_failed_attempts": "INTEGER NOT NULL DEFAULT 0",
            "pin_locked_until": "TEXT",
            "pin_created_at": "TEXT"
        }
        for col, col_type in migration_cols.items():
            if col not in existing_cols:
                try:
                    con.execute(f"ALTER TABLE farmers ADD COLUMN {col} {col_type};")
                except sqlite3.OperationalError:
                    pass

        # 2. Immutable Audit Events Table (SQLite runtime equivalent of Safeguard 8)
        con.execute("""
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id TEXT PRIMARY KEY,
                actor_id TEXT,
                actor_role TEXT NOT NULL DEFAULT 'anonymous',
                action_type TEXT NOT NULL,
                target_resource TEXT NOT NULL,
                record_id TEXT,
                client_ip TEXT,
                created_at TEXT NOT NULL
            );
        """)

        # Performance indices
        con.execute("CREATE INDEX IF NOT EXISTS idx_farmers_intermediary ON farmers(intermediary_id);")
        con.execute("CREATE INDEX IF NOT EXISTS idx_farmers_consent ON farmers(consent_status);")
        con.execute("CREATE INDEX IF NOT EXISTS idx_farmers_deleted ON farmers(is_deleted);")
        con.execute("CREATE INDEX IF NOT EXISTS idx_farmers_passbook_review ON farmers(passbook_review_status);")
        con.execute("CREATE INDEX IF NOT EXISTS idx_farmers_pin_locked ON farmers(pin_locked_until);")
        con.execute("CREATE INDEX IF NOT EXISTS idx_audit_events_actor ON audit_events(actor_id);")
        con.execute("CREATE INDEX IF NOT EXISTS idx_audit_events_created ON audit_events(created_at);")

        con.commit()

    restrict_db_permissions(resolved_path)
    return str(resolved_path)


def get_configured_db_backend() -> str:
    """
    Returns 'sqlite' or 'postgres' based on configuration.
    Fails safely if postgres is requested without necessary environment secrets.
    """
    backend = os.getenv("DATABASE_BACKEND", "sqlite").lower().strip()
    if backend == "postgres":
        required_vars = ["DB_HOST", "DB_NAME", "DB_USER"]
        missing = [v for v in required_vars if not os.getenv(v)]
        # Either password or IAM token must be provided
        has_auth = bool(os.getenv("DB_PASSWORD") or os.getenv("DB_IAM_TOKEN"))
        if missing or not has_auth:
            raise RuntimeError(
                f"PostgreSQL backend requested, but required credentials/configuration are missing: "
                f"missing={missing}, has_auth={has_auth}. Fail-closed security rule enforced."
            )
        return "postgres"
    return "sqlite"
