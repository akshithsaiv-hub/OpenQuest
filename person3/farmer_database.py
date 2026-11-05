"""
farmer_database.py
==================
Database connection and initialization module for Person 3 backend.
Manages SQLite storage for farmer profiles with automated schema setup.

Privacy Guidelines:
- Stores only minimum necessary personal data.
- NEVER stores raw Aadhaar numbers or scans.
- Default storage: database/farmer_data.db
"""

import os
import sqlite3
from pathlib import Path

# Default path relative to workspace or current execution context
DEFAULT_DB_DIR = Path("database")
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "farmer_data.db"


def get_db_path(custom_path=None) -> Path:
    """
    Resolve and return database path.
    Ensures parent directory exists.
    """
    if custom_path:
        path = Path(custom_path)
    else:
        # Check environment variable or fallback to default
        env_path = os.getenv("FARMER_DB_PATH")
        path = Path(env_path) if env_path else DEFAULT_DB_PATH

    # Ensure the parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect(db_path=None) -> sqlite3.Connection:
    """
    Establish connection to SQLite database with Row factory enabled.
    """
    resolved_path = get_db_path(db_path)
    con = sqlite3.connect(resolved_path)
    con.row_factory = sqlite3.Row
    # Enable foreign keys and WAL mode for better concurrency
    con.execute("PRAGMA foreign_keys = ON;")
    return con


def init_db(db_path=None):
    """
    Initialize SQLite database tables and indices automatically.
    Safe to call multiple times (IF NOT EXISTS).
    """
    resolved_path = get_db_path(db_path)
    with connect(resolved_path) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id TEXT PRIMARY KEY,
                farmer_name TEXT NOT NULL,
                phone_number TEXT,
                preferred_language TEXT DEFAULT 'te',
                intermediary_id TEXT,
                consent_status INTEGER NOT NULL CHECK (consent_status IN (0, 1)),
                uploaded_documents TEXT NOT NULL DEFAULT '{}',
                bank_account_name TEXT,
                created_at TEXT NOT NULL
            );
        """)

        # Performance indices for quick filtering by intermediary and consent status
        con.execute("""
            CREATE INDEX IF NOT EXISTS idx_farmers_intermediary 
            ON farmers(intermediary_id);
        """)
        con.execute("""
            CREATE INDEX IF NOT EXISTS idx_farmers_consent 
            ON farmers(consent_status);
        """)
        con.commit()
    return str(resolved_path)
