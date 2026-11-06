-- ==============================================================================
-- Migration 002: Farmer Passbook Document Wallet & Argon2id PIN Security
-- ==============================================================================
-- Hardens OpenQuest Document Wallet to support strictly Farmer Passbook records
-- and enforces Argon2id salted password hashing with persistent brute-force lockout
-- for passbook review requests.
-- ==============================================================================

-- 1. Extend farmers table with passbook metadata and PIN lockout columns
ALTER TABLE farmers ADD COLUMN passbook_saved INTEGER NOT NULL DEFAULT 0;
ALTER TABLE farmers ADD COLUMN passbook_filename TEXT;
ALTER TABLE farmers ADD COLUMN passbook_uploaded_at TEXT;
ALTER TABLE farmers ADD COLUMN passbook_data TEXT;
ALTER TABLE farmers ADD COLUMN passbook_review_status TEXT DEFAULT 'not_requested';
ALTER TABLE farmers ADD COLUMN passbook_reviewed_at TEXT;
ALTER TABLE farmers ADD COLUMN passbook_reviewer_id TEXT;
ALTER TABLE farmers ADD COLUMN pin_hash TEXT;
ALTER TABLE farmers ADD COLUMN pin_salt TEXT;
ALTER TABLE farmers ADD COLUMN pin_failed_attempts INTEGER NOT NULL DEFAULT 0;
ALTER TABLE farmers ADD COLUMN pin_locked_until TEXT;
ALTER TABLE farmers ADD COLUMN pin_created_at TEXT;

-- 2. Performance & Security Indexes
CREATE INDEX IF NOT EXISTS idx_farmers_passbook_review ON farmers(passbook_review_status);
CREATE INDEX IF NOT EXISTS idx_farmers_pin_locked ON farmers(pin_locked_until);
