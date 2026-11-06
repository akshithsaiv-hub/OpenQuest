-- ============================================================================
-- File: sanitize_nonprod.sql
-- Description: Database Sanitization Script for Non-Production Environments
--              (Staging, QA, Development, CI/CD).
-- Author: Senior Database Architect & Security Engineer
-- Objective: Scrub all Direct Identifiers (PII), contact information, and audit
--            telemetry while preserving relational integrity and demographic
--            distribution for testing.
-- ============================================================================

BEGIN;

-- Verify environment safety check to prevent accidental execution in Production
DO $$
DECLARE
    v_env VARCHAR(64);
BEGIN
    v_env := COALESCE(current_setting('app.environment', true), 'UNKNOWN');
    IF v_env = 'production' OR v_env = 'prod' THEN
        RAISE EXCEPTION 'FATAL: Cannot execute sanitization script against a PRODUCTION database environment!';
    END IF;
    RAISE NOTICE 'Starting database sanitization for environment: %', v_env;
END $$;

-- ----------------------------------------------------------------------------
-- 1. Sanitize Master Farmers Table
-- ----------------------------------------------------------------------------
UPDATE public.farmers
SET 
    -- Deterministic mock names based on UUID hash to prevent individual linkage
    display_name = 'Dev_Farmer_' || SUBSTRING(farmer_id::text, 1, 8),
    -- Clear raw encrypted phone payloads
    phone_encrypted = NULL,
    phone_last4 = '9999',
    -- Replace identity hash with synthetic non-reversible mock hashes
    identity_hash = encode(digest('MOCK_IDENTITY_' || farmer_id::text, 'sha256'), 'hex'),
    -- Synthetic banking tokens
    bank_account_token = gen_random_uuid(),
    bank_ifsc_masked = 'SBIN0000000',
    -- Snap village coordinates to generalized synthetic center
    village = 'MOCK_VILLAGE_' || SUBSTRING(farmer_id::text, 1, 4),
    updated_at = clock_timestamp();

RAISE NOTICE 'Farmers table sanitized successfully.';

-- ----------------------------------------------------------------------------
-- 2. Sanitize User Consents Table
-- ----------------------------------------------------------------------------
UPDATE public.user_consents
SET 
    client_ip = '127.0.0.1'::inet,
    user_agent = 'Mozilla/5.0 (Sanitized Staging Test Runner)';

RAISE NOTICE 'User consents table sanitized successfully.';

-- ----------------------------------------------------------------------------
-- 3. Sanitize Crop Claims Geo-Coordinates (Remove Exact Farm Boundary Evidence)
-- ----------------------------------------------------------------------------
UPDATE public.crop_claims
SET 
    -- Jitter coordinates within a 1km bounding box or snap to district baseline
    geo_latitude = ROUND(geo_latitude, 2),
    geo_longitude = ROUND(geo_longitude, 2)
WHERE geo_latitude IS NOT NULL;

RAISE NOTICE 'Crop claims spatial coordinates sanitized successfully.';

-- ----------------------------------------------------------------------------
-- 4. Sanitize Document Verification Hashes
-- ----------------------------------------------------------------------------
UPDATE public.document_metadata
SET 
    sha256_hash = encode(digest('MOCK_DOC_' || doc_id::text, 'sha256'), 'hex');

RAISE NOTICE 'Document metadata hashes sanitized successfully.';

-- ----------------------------------------------------------------------------
-- 5. Anonymize Operational Audit Logs Telemetry
-- ----------------------------------------------------------------------------
-- Temporarily bypass the audit tampering trigger for non-prod scrubbing
ALTER TABLE public.audit_logs DISABLE TRIGGER trg_prevent_audit_tampering;

UPDATE public.audit_logs
SET 
    client_ip = '10.0.0.1'::inet,
    application_name = 'Sanitized Non-Production Harness',
    old_values = CASE 
        WHEN old_values IS NOT NULL THEN jsonb_build_object('sanitized', true)
        ELSE NULL 
    END,
    new_values = CASE 
        WHEN new_values IS NOT NULL THEN jsonb_build_object('sanitized', true)
        ELSE NULL 
    END;

ALTER TABLE public.audit_logs ENABLE TRIGGER trg_prevent_audit_tampering;

RAISE NOTICE 'Audit logs telemetry sanitized successfully.';

COMMIT;
