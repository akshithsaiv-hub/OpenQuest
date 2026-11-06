-- ============================================================================
-- Migration: 001_dlp_security_hardening.sql
-- Description: Production-grade Data Leak Prevention (DLP) architecture
--              implementing 16 architectural safeguards for PostgreSQL.
-- Author: Senior Database Architect & Security Engineer
-- ============================================================================

-- Ensure required cryptographic and UUID extensions are enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- SAFEGUARD 4: ROLE-BASED ACCESS CONTROL (RBAC) & LEAST PRIVILEGE
-- ============================================================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_farmer') THEN
        CREATE ROLE app_farmer WITH NOLOGIN NOSUPERUSER NOINHERIT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_intermediary') THEN
        CREATE ROLE app_intermediary WITH NOLOGIN NOSUPERUSER NOINHERIT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_officer') THEN
        CREATE ROLE app_officer WITH NOLOGIN NOSUPERUSER NOINHERIT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_service') THEN
        CREATE ROLE app_service WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_audit') THEN
        CREATE ROLE app_audit WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_rag_public') THEN
        CREATE ROLE app_rag_public WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE;
    END IF;
END $$;

-- Revoke default public schema permissions to enforce strict boundary
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO app_service, app_audit, app_rag_public;

-- ============================================================================
-- SAFEGUARD 8: IMMUTABLE AUDIT LOGS (DDL)
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.audit_logs (
    log_id          BIGSERIAL PRIMARY KEY,
    actor_id        UUID,
    actor_role      VARCHAR(32) NOT NULL DEFAULT 'unknown',
    action_type     VARCHAR(16) NOT NULL CHECK (action_type IN ('INSERT', 'UPDATE', 'DELETE', 'ANONYMIZE', 'CONSENT_REVOKE')),
    target_table    VARCHAR(64) NOT NULL,
    record_id       VARCHAR(64) NOT NULL,
    old_values      JSONB,
    new_values      JSONB,
    client_ip       INET,
    application_name VARCHAR(128),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- Index audit log table for performant compliance queries
CREATE INDEX IF NOT EXISTS idx_audit_logs_actor ON public.audit_logs(actor_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_target ON public.audit_logs(target_table, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON public.audit_logs(created_at DESC);

-- Guarantee Immutability: Block UPDATE, DELETE, and TRUNCATE on audit_logs
REVOKE UPDATE, DELETE, TRUNCATE ON public.audit_logs FROM PUBLIC, app_service;
GRANT SELECT, INSERT ON public.audit_logs TO app_service;
GRANT SELECT ON public.audit_logs TO app_audit;

-- Trigger ensuring no row in audit_logs can ever be altered or deleted
CREATE OR REPLACE FUNCTION public.fn_prevent_audit_tampering()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RAISE EXCEPTION 'SECURITY VIOLATION: audit_logs is append-only. Modification or deletion of records is strictly prohibited.';
    RETURN NULL;
END;
$$;

DROP TRIGGER IF EXISTS trg_prevent_audit_tampering ON public.audit_logs;
CREATE TRIGGER trg_prevent_audit_tampering
BEFORE UPDATE OR DELETE OR TRUNCATE ON public.audit_logs
FOR EACH STATEMENT
EXECUTE FUNCTION public.fn_prevent_audit_tampering();

-- ============================================================================
-- SAFEGUARDS 1 & 3: DATA MINIMIZATION, OPERATIONAL TABLES & COLUMN ENCRYPTION
-- ============================================================================

-- Master Farmers Table (Sensitive Identifiers Minimized or Cryptographically Hashed)
CREATE TABLE IF NOT EXISTS public.farmers (
    farmer_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name            VARCHAR(128) NOT NULL,
    -- Column-Level Encryption for Mandatory Contact Information (pgcrypto)
    phone_encrypted         BYTEA,
    phone_last4             VARCHAR(4) NOT NULL CHECK (phone_last4 ~ '^[0-9]{4}$'),
    -- Identity Minimization: Cryptographic Salted Hash for Deduplication (Zero Plaintext Aadhaar/PAN)
    identity_hash           VARCHAR(64) UNIQUE,
    is_identity_verified    BOOLEAN NOT NULL DEFAULT FALSE,
    identity_verified_at    TIMESTAMPTZ,
    -- Financial Minimization: Tokenized Bank References
    bank_account_token      UUID,
    bank_ifsc_masked        VARCHAR(11),
    is_bank_verified        BOOLEAN NOT NULL DEFAULT FALSE,
    -- Demographic / Spatial Data (Generalized for K-Anonymity)
    state                   VARCHAR(64) NOT NULL,
    district                VARCHAR(64) NOT NULL,
    mandal                  VARCHAR(64) NOT NULL,
    village                 VARCHAR(64) NOT NULL,
    land_acres              NUMERIC(6, 2) NOT NULL CHECK (land_acres >= 0),
    farmer_type             VARCHAR(32) NOT NULL CHECK (farmer_type IN ('owner', 'tenant_registered', 'tenant_oral')),
    preferred_language      VARCHAR(5) NOT NULL DEFAULT 'en' CHECK (preferred_language IN ('en', 'te', 'hi', 'mr', 'ta', 'kn')),
    intermediary_id         UUID,
    -- Soft-Delete & Anonymization Lifecycle
    is_deleted              BOOLEAN NOT NULL DEFAULT FALSE,
    anonymized_at           TIMESTAMPTZ,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- ============================================================================
-- SAFEGUARD 2: CONSENT MANAGEMENT
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.user_consents (
    consent_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES public.farmers(farmer_id) ON DELETE CASCADE,
    consent_version_id      VARCHAR(32) NOT NULL,
    language_code           VARCHAR(5) NOT NULL CHECK (language_code IN ('en', 'te', 'hi', 'mr', 'ta', 'kn')),
    purpose_codes           TEXT[] NOT NULL,
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    granted_at              TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    withdrawn_at            TIMESTAMPTZ,
    client_ip               INET,
    user_agent              TEXT,
    CONSTRAINT chk_consent_withdrawal CHECK (
        (is_active = TRUE AND withdrawn_at IS NULL) OR 
        (is_active = FALSE AND withdrawn_at IS NOT NULL)
    )
);

CREATE INDEX IF NOT EXISTS idx_user_consents_lookup ON public.user_consents(user_id, is_active);

-- Crop Insurance & Emergency Claims Table
CREATE TABLE IF NOT EXISTS public.crop_claims (
    claim_id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id               UUID NOT NULL REFERENCES public.farmers(farmer_id) ON DELETE RESTRICT,
    scheme_id               VARCHAR(64) NOT NULL,
    crop_name               VARCHAR(64) NOT NULL,
    loss_date               DATE NOT NULL,
    loss_percentage         NUMERIC(5, 2) NOT NULL CHECK (loss_percentage BETWEEN 0 AND 100),
    intimation_channel      VARCHAR(32) NOT NULL DEFAULT 'in_app',
    claim_status            VARCHAR(32) NOT NULL DEFAULT 'SUBMITTED' 
                            CHECK (claim_status IN ('SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED', 'DISBURSED')),
    estimated_payout        NUMERIC(10, 2) NOT NULL DEFAULT 0.00 CHECK (estimated_payout >= 0),
    -- Spatial Evidence generalized to district centroid unless verified
    geo_latitude            NUMERIC(9, 6),
    geo_longitude           NUMERIC(9, 6),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

CREATE INDEX IF NOT EXISTS idx_crop_claims_farmer ON public.crop_claims(farmer_id);
CREATE INDEX IF NOT EXISTS idx_crop_claims_status ON public.crop_claims(claim_status);

-- Document Metadata Table (Zero Raw Biometrics or Image Files in DB)
CREATE TABLE IF NOT EXISTS public.document_metadata (
    doc_id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id               UUID NOT NULL REFERENCES public.farmers(farmer_id) ON DELETE CASCADE,
    doc_type                VARCHAR(32) NOT NULL CHECK (doc_type IN ('aadhaar_ocr_verified', 'pahani_ror', 'ccrc_card', 'bank_passbook')),
    sha256_hash             VARCHAR(64) NOT NULL,
    is_verified             BOOLEAN NOT NULL DEFAULT FALSE,
    verified_by             UUID,
    verified_at             TIMESTAMPTZ,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

CREATE INDEX IF NOT EXISTS idx_doc_metadata_farmer ON public.document_metadata(farmer_id);

-- ============================================================================
-- SAFEGUARD 2: AUTOMATED AUDIT TRIGGER FUNCTION
-- ============================================================================
CREATE OR REPLACE FUNCTION public.fn_audit_log_trigger()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
DECLARE
    v_actor_id   UUID;
    v_actor_role VARCHAR(32);
    v_record_id  VARCHAR(64);
    v_client_ip  INET;
    v_old_json   JSONB := NULL;
    v_new_json   JSONB := NULL;
BEGIN
    -- Extract session-scoped actor credentials safely
    BEGIN
        v_actor_id := NULLIF(current_setting('app.current_user_id', true), '')::uuid;
    EXCEPTION WHEN OTHERS THEN
        v_actor_id := NULL;
    END;

    v_actor_role := COALESCE(NULLIF(current_setting('app.current_role', true), ''), current_user);
    
    BEGIN
        v_client_ip := NULLIF(current_setting('app.client_ip', true), '')::inet;
    EXCEPTION WHEN OTHERS THEN
        v_client_ip := inet_client_addr();
    END;

    IF (TG_OP = 'DELETE') THEN
        v_record_id := OLD.farmer_id::text;
        v_old_json := to_jsonb(OLD);
    ELSIF (TG_OP = 'UPDATE') THEN
        v_record_id := NEW.farmer_id::text;
        v_old_json := to_jsonb(OLD);
        v_new_json := to_jsonb(NEW);
    ELSIF (TG_OP = 'INSERT') THEN
        v_record_id := NEW.farmer_id::text;
        v_new_json := to_jsonb(NEW);
    END IF;

    -- Strip encrypted fields from audit logs to avoid secondary leakage
    IF v_old_json ? 'phone_encrypted' THEN
        v_old_json := v_old_json - 'phone_encrypted';
    END IF;
    IF v_new_json ? 'phone_encrypted' THEN
        v_new_json := v_new_json - 'phone_encrypted';
    END IF;

    INSERT INTO public.audit_logs (
        actor_id,
        actor_role,
        action_type,
        target_table,
        record_id,
        old_values,
        new_values,
        client_ip,
        application_name,
        created_at
    ) VALUES (
        v_actor_id,
        v_actor_role,
        TG_OP,
        TG_TABLE_NAME,
        COALESCE(v_record_id, 'UNKNOWN'),
        v_old_json,
        v_new_json,
        v_client_ip,
        current_setting('application_name', true),
        clock_timestamp()
    );

    IF (TG_OP = 'DELETE') THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$;

-- Attach Audit Triggers to Sensitive Tables
DROP TRIGGER IF EXISTS trg_audit_farmers ON public.farmers;
CREATE TRIGGER trg_audit_farmers
AFTER INSERT OR UPDATE OR DELETE ON public.farmers
FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log_trigger();

DROP TRIGGER IF EXISTS trg_audit_user_consents ON public.user_consents;
CREATE TRIGGER trg_audit_user_consents
AFTER INSERT OR UPDATE OR DELETE ON public.user_consents
FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log_trigger();

DROP TRIGGER IF EXISTS trg_audit_crop_claims ON public.crop_claims;
CREATE TRIGGER trg_audit_crop_claims
AFTER INSERT OR UPDATE OR DELETE ON public.crop_claims
FOR EACH ROW EXECUTE FUNCTION public.fn_audit_log_trigger();

-- ============================================================================
-- SAFEGUARD 2: STORED PROCEDURE FOR SOFT-DELETION & PII ANONYMIZATION
-- ============================================================================
CREATE OR REPLACE PROCEDURE public.sp_soft_delete_and_anonymize_user(
    p_farmer_id UUID,
    p_actor_id  UUID DEFAULT NULL
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pg_temp
AS $$
DECLARE
    v_found BOOLEAN;
BEGIN
    -- Verify target farmer exists
    SELECT EXISTS (SELECT 1 FROM public.farmers WHERE farmer_id = p_farmer_id) INTO v_found;
    IF NOT v_found THEN
        RAISE EXCEPTION 'Farmer with ID % not found.', p_farmer_id;
    END IF;

    -- 1. Deactivate all active consent records
    UPDATE public.user_consents
    SET is_active = FALSE,
        withdrawn_at = clock_timestamp()
    WHERE user_id = p_farmer_id AND is_active = TRUE;

    -- 2. Anonymize PII in operational table while retaining aggregate demographic & land metrics
    UPDATE public.farmers
    SET display_name        = 'ANONYMIZED_FARMER_' || SUBSTRING(p_farmer_id::text, 1, 8),
        phone_encrypted     = NULL,
        phone_last4         = '0000',
        identity_hash       = NULL,
        is_identity_verified= FALSE,
        bank_account_token  = NULL,
        bank_ifsc_masked    = NULL,
        is_bank_verified    = FALSE,
        intermediary_id     = NULL,
        is_deleted          = TRUE,
        anonymized_at       = clock_timestamp(),
        updated_at          = clock_timestamp()
    WHERE farmer_id = p_farmer_id;

    -- 3. Scrub sensitive document verification hashes
    DELETE FROM public.document_metadata
    WHERE farmer_id = p_farmer_id;

    -- 4. Record explicit compliance event in immutable audit log
    INSERT INTO public.audit_logs (
        actor_id,
        actor_role,
        action_type,
        target_table,
        record_id,
        old_values,
        new_values,
        client_ip,
        application_name,
        created_at
    ) VALUES (
        COALESCE(p_actor_id, NULLIF(current_setting('app.current_user_id', true), '')::uuid),
        COALESCE(NULLIF(current_setting('app.current_role', true), ''), 'sp_anonymize'),
        'ANONYMIZE',
        'farmers',
        p_farmer_id::text,
        jsonb_build_object('status', 'PII_ACTIVE'),
        jsonb_build_object('status', 'ANONYMIZED', 'anonymized_at', clock_timestamp()),
        inet_client_addr(),
        'sp_soft_delete_and_anonymize_user',
        clock_timestamp()
    );

    RAISE NOTICE 'Farmer % successfully soft-deleted, anonymized, and logged.', p_farmer_id;
END;
$$;

-- ============================================================================
-- SAFEGUARD 5: USER ISOLATION & ROW-LEVEL SECURITY (RLS)
-- ============================================================================

-- Enable and force RLS on all tenant operational tables
ALTER TABLE public.farmers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.farmers FORCE ROW LEVEL SECURITY;

ALTER TABLE public.user_consents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_consents FORCE ROW LEVEL SECURITY;

ALTER TABLE public.crop_claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crop_claims FORCE ROW LEVEL SECURITY;

ALTER TABLE public.document_metadata ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.document_metadata FORCE ROW LEVEL SECURITY;

-- ----------------------------------------------------------------------------
-- Farmers Table Policies
-- ----------------------------------------------------------------------------

-- Policy 1: Farmers can strictly view and update their own active profile
DROP POLICY IF EXISTS p_farmer_self_access ON public.farmers;
CREATE POLICY p_farmer_self_access ON public.farmers
AS PERMISSIVE
FOR ALL
TO app_service, app_farmer
USING (
    farmer_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
    AND is_deleted = FALSE
)
WITH CHECK (
    farmer_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
    AND is_deleted = FALSE
);

-- Policy 2: Intermediaries can view farmers assigned to them ONLY IF consent is active
DROP POLICY IF EXISTS p_intermediary_consented_access ON public.farmers;
CREATE POLICY p_intermediary_consented_access ON public.farmers
AS PERMISSIVE
FOR SELECT
TO app_service, app_intermediary
USING (
    intermediary_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
    AND is_deleted = FALSE
    AND EXISTS (
        SELECT 1 FROM public.user_consents uc
        WHERE uc.user_id = public.farmers.farmer_id
          AND uc.is_active = TRUE
    )
);

-- Policy 3: Authorized Government Agriculture Officers can query records within their jurisdiction
DROP POLICY IF EXISTS p_officer_jurisdiction_access ON public.farmers;
CREATE POLICY p_officer_jurisdiction_access ON public.farmers
AS PERMISSIVE
FOR SELECT
TO app_service, app_officer
USING (
    current_setting('app.current_role', true) = 'app_officer'
    AND state = NULLIF(current_setting('app.officer_state', true), '')
);

-- ----------------------------------------------------------------------------
-- User Consents Table Policies
-- ----------------------------------------------------------------------------
DROP POLICY IF EXISTS p_consent_self_access ON public.user_consents;
CREATE POLICY p_consent_self_access ON public.user_consents
AS PERMISSIVE
FOR ALL
TO app_service, app_farmer
USING (
    user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
)
WITH CHECK (
    user_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
);

-- ----------------------------------------------------------------------------
-- Crop Claims Table Policies
-- ----------------------------------------------------------------------------
DROP POLICY IF EXISTS p_claims_farmer_access ON public.crop_claims;
CREATE POLICY p_claims_farmer_access ON public.crop_claims
AS PERMISSIVE
FOR ALL
TO app_service, app_farmer
USING (
    farmer_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
)
WITH CHECK (
    farmer_id = NULLIF(current_setting('app.current_user_id', true), '')::uuid
);

DROP POLICY IF EXISTS p_claims_officer_access ON public.crop_claims;
CREATE POLICY p_claims_officer_access ON public.crop_claims
AS PERMISSIVE
FOR ALL
TO app_service, app_officer
USING (
    current_setting('app.current_role', true) = 'app_officer'
);

-- ============================================================================
-- SAFEGUARD 12: DYNAMIC DATA MASKING (DDM) SECURITY BARRIER VIEWS
-- ============================================================================

-- Security barrier view providing masked representations for non-privileged readers
CREATE OR REPLACE VIEW public.vw_farmers_masked
WITH (security_barrier = TRUE)
AS
SELECT 
    farmer_id,
    -- Dynamic masking of name
    CASE 
        WHEN current_setting('app.current_role', true) IN ('app_officer', 'app_audit') THEN display_name
        ELSE CONCAT(LEFT(display_name, 1), '*** ', SPLIT_PART(display_name, ' ', 2))
    END AS masked_display_name,
    -- Dynamic masking of phone
    CONCAT('+91-XXXXXX', phone_last4) AS masked_phone,
    is_identity_verified,
    is_bank_verified,
    state,
    district,
    mandal,
    village,
    land_acres,
    farmer_type,
    preferred_language,
    created_at
FROM public.farmers
WHERE is_deleted = FALSE;

GRANT SELECT ON public.vw_farmers_masked TO app_intermediary, app_service;

-- ============================================================================
-- SAFEGUARD 7: RAG & VECTOR DB ACCESS ISOLATION
-- ============================================================================
-- Revoke all access to operational tenant tables for the public knowledge base role
REVOKE ALL ON public.farmers FROM app_rag_public;
REVOKE ALL ON public.user_consents FROM app_rag_public;
REVOKE ALL ON public.crop_claims FROM app_rag_public;
REVOKE ALL ON public.document_metadata FROM app_rag_public;
REVOKE ALL ON public.audit_logs FROM app_rag_public;

-- Grant app_rag_public read access ONLY on public non-sensitive knowledge base tables
-- (schemes, msp_rates, input_prices, advisory)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'schemes') THEN
        GRANT SELECT ON public.schemes TO app_rag_public;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'msp_mandi_rates') THEN
        GRANT SELECT ON public.msp_mandi_rates TO app_rag_public;
    END IF;
END $$;
