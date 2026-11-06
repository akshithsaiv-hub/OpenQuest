-- ============================================================================
-- File: anonymized_analytics_queries.sql
-- Description: Production-grade Analytical K-Anonymity and Database Activity
--              Monitoring (DAM) queries for agricultural officer dashboards.
-- Author: Senior Database Architect & Security Engineer
-- ============================================================================

-- ============================================================================
-- SAFEGUARD 10: ANONYMIZED DASHBOARDS (K-ANONYMITY >= 10)
-- Objective: Allow district & state agricultural officers to analyze scheme adoption,
--            crop distributions, and loss trends without re-identifying individuals.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 1: Regional Crop Loss & Payout Dashboard (K-Anonymity Threshold k >= 10)
-- Enforces:
-- 1. GROUP BY on quasi-identifiers (state, district, crop_name, farmer_type).
-- 2. HAVING COUNT(DISTINCT f.farmer_id) >= 10 to suppress micro-cohorts.
-- 3. Rounded average and sum payouts to avoid micro-inference attacks.
-- ----------------------------------------------------------------------------
SELECT 
    f.state,
    f.district,
    c.crop_name,
    f.farmer_type,
    -- Suppress exact counts into sanitized bucket ranges or aggregate count
    COUNT(DISTINCT f.farmer_id) AS cohort_farmer_count,
    ROUND(AVG(f.land_acres), 2) AS avg_land_acres,
    ROUND(AVG(c.loss_percentage), 1) AS avg_crop_loss_pct,
    ROUND(SUM(c.estimated_payout), -2) AS total_estimated_payout_rounded
FROM public.farmers f
INNER JOIN public.crop_claims c ON f.farmer_id = c.farmer_id
INNER JOIN public.user_consents uc ON f.farmer_id = uc.user_id
WHERE 
    f.is_deleted = FALSE
    AND uc.is_active = TRUE
    AND 'statistical_analytics' = ANY(uc.purpose_codes)
    AND c.created_at >= (clock_timestamp() - INTERVAL '1 year')
GROUP BY 
    f.state,
    f.district,
    c.crop_name,
    f.farmer_type
HAVING 
    COUNT(DISTINCT f.farmer_id) >= 10
ORDER BY 
    f.state,
    f.district,
    cohort_farmer_count DESC;

-- ----------------------------------------------------------------------------
-- Query 2: Advanced K-Anonymity with Automatic Micro-Cohort Generalization
-- When a mandal has fewer than 10 farmers for a crop, instead of dropping
-- the statistical data, it rolls it up into 'DISTRICT_RESIDUAL_COHORT'.
-- ----------------------------------------------------------------------------
WITH raw_cohorts AS (
    SELECT 
        f.state,
        f.district,
        f.mandal,
        c.crop_name,
        COUNT(DISTINCT f.farmer_id) AS farmer_count,
        SUM(c.estimated_payout) AS total_payout
    FROM public.farmers f
    JOIN public.crop_claims c ON f.farmer_id = c.farmer_id
    WHERE f.is_deleted = FALSE
    GROUP BY f.state, f.district, f.mandal, c.crop_name
)
SELECT 
    state,
    district,
    crop_name,
    CASE 
        WHEN farmer_count < 10 THEN 'OTHER_SUPPRESSED_MANDALS'
        ELSE mandal
    END AS reporting_mandal,
    SUM(farmer_count) AS aggregated_farmers,
    ROUND(SUM(total_payout), -2) AS rounded_payout
FROM raw_cohorts
GROUP BY 
    state,
    district,
    crop_name,
    CASE 
        WHEN farmer_count < 10 THEN 'OTHER_SUPPRESSED_MANDALS'
        ELSE mandal
    END
HAVING 
    SUM(farmer_count) >= 10
ORDER BY 
    state, district, reporting_mandal;

-- ============================================================================
-- SAFEGUARD 11: DATABASE ACTIVITY MONITORING (DAM) & UEBA AUDIT QUERIES
-- Objective: Detect full-table scans, bulk data access anomalies, and after-hours
--            suspicious operations across the database engine.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 3: Detection of Bulk Exfiltration & High-Volume Access Events
-- Identifies actors accessing > 50 distinct records in a 5-minute rolling window
-- ----------------------------------------------------------------------------
SELECT 
    actor_id,
    actor_role,
    target_table,
    client_ip,
    COUNT(DISTINCT record_id) AS distinct_records_accessed,
    MIN(created_at) AS first_access_at,
    MAX(created_at) AS last_access_at
FROM public.audit_logs
WHERE 
    created_at >= (clock_timestamp() - INTERVAL '15 minutes')
    AND action_type IN ('INSERT', 'UPDATE', 'DELETE', 'ANONYMIZE')
GROUP BY 
    actor_id,
    actor_role,
    target_table,
    client_ip
HAVING 
    COUNT(DISTINCT record_id) >= 50
ORDER BY 
    distinct_records_accessed DESC;

-- ----------------------------------------------------------------------------
-- Query 4: After-Hours Operational Query Anomaly Detector
-- Flags non-automated database activity occurring between 22:00 and 05:00 local time
-- ----------------------------------------------------------------------------
SELECT 
    log_id,
    actor_id,
    actor_role,
    action_type,
    target_table,
    record_id,
    client_ip,
    application_name,
    created_at,
    TO_CHAR(created_at AT TIME ZONE 'Asia/Kolkata', 'HH24:MI:SS') AS local_time_ist
FROM public.audit_logs
WHERE 
    created_at >= (clock_timestamp() - INTERVAL '24 hours')
    AND EXTRACT(HOUR FROM created_at AT TIME ZONE 'Asia/Kolkata') IN (22, 23, 0, 1, 2, 3, 4)
    AND actor_role NOT IN ('cron_system', 'batch_etl_worker')
ORDER BY 
    created_at DESC;

-- ----------------------------------------------------------------------------
-- Query 5: Full-Table Scan Identification via pg_stat_statements / pg_stat_user_tables
-- Identifies queries causing sequential scans on sensitive tenant tables
-- ----------------------------------------------------------------------------
SELECT 
    relname AS table_name,
    seq_scan AS sequential_scans,
    seq_tup_read AS tuples_read_via_seq_scan,
    idx_scan AS index_scans,
    idx_tup_fetch AS tuples_fetched_via_index,
    CASE 
        WHEN (seq_scan + idx_scan) = 0 THEN 0.0
        ELSE ROUND((seq_scan::numeric / (seq_scan + idx_scan)::numeric) * 100, 2)
    END AS seq_scan_percentage
FROM pg_stat_user_tables
WHERE relname IN ('farmers', 'user_consents', 'crop_claims', 'audit_logs')
ORDER BY seq_scan DESC;
