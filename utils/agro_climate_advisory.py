"""
Agro-Climatic Intelligence & Crop Migration Ecosystem
Provides dynamic near-future weather guidance, drought & dry-spell early warnings,
smart micro-irrigation (Drip/Sprinkler) Buy vs Rent subsidy matchmaker,
and routine crop migration analysis.
"""

from typing import Dict, Any, List, Optional

# District Agro-Climatic Weather Profiles
DISTRICT_WEATHER_PROFILES: Dict[str, Dict[str, Any]] = {
    "Telangana": {
        "Warangal": {
            "rainfall_deficit_pct": -46,
            "forecast_14d_rainfall_mm": 12.5,
            "soil_moisture_pct": 18,
            "max_temp_c": 37.8,
            "dry_spell_days": 19,
            "drought_alert_level": "CRITICAL",
            "groundwater_status": "Over-Exploited / Semi-Critical",
            "forecast_daily": [
                {"day": "Day 1", "temp": "37°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry"},
                {"day": "Day 2", "temp": "38°C", "rain_prob": "0%", "icon": "☀️", "status": "Dry"},
                {"day": "Day 3", "temp": "38°C", "rain_prob": "0%", "icon": "☀️", "status": "Hot"},
                {"day": "Day 4", "temp": "37°C", "rain_prob": "10%", "icon": "⛅", "status": "Partly Cloudy"},
                {"day": "Day 5", "temp": "39°C", "rain_prob": "0%", "icon": "🔥", "status": "Heatwave"},
                {"day": "Day 6", "temp": "38°C", "rain_prob": "0%", "icon": "☀️", "status": "Dry"},
                {"day": "Day 7", "temp": "36°C", "rain_prob": "15%", "icon": "🌦️", "status": "Isolated Light Rain"},
                {"day": "Day 8-14", "temp": "37°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry Spell Extends"}
            ]
        },
        "Karimnagar": {
            "rainfall_deficit_pct": -38,
            "forecast_14d_rainfall_mm": 18.0,
            "soil_moisture_pct": 22,
            "max_temp_c": 36.5,
            "dry_spell_days": 15,
            "drought_alert_level": "SEVERE",
            "groundwater_status": "Semi-Critical",
            "forecast_daily": [
                {"day": "Day 1-3", "temp": "36°C", "rain_prob": "10%", "icon": "☀️", "status": "Dry"},
                {"day": "Day 4-7", "temp": "37°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry"},
                {"day": "Day 8-14", "temp": "36°C", "rain_prob": "10%", "icon": "⛅", "status": "Mild Stress"}
            ]
        },
        "Nalgonda": {
            "rainfall_deficit_pct": -52,
            "forecast_14d_rainfall_mm": 8.0,
            "soil_moisture_pct": 14,
            "max_temp_c": 39.2,
            "dry_spell_days": 24,
            "drought_alert_level": "CRITICAL",
            "groundwater_status": "Critical / Saline Intrusion",
            "forecast_daily": [
                {"day": "Day 1-4", "temp": "39°C", "rain_prob": "0%", "icon": "🔥", "status": "Severe Heat"},
                {"day": "Day 5-10", "temp": "38°C", "rain_prob": "5%", "icon": "☀️", "status": "Acute Dry Spell"},
                {"day": "Day 11-14", "temp": "37°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry"}
            ]
        },
        "Mahabubnagar": {
            "rainfall_deficit_pct": -48,
            "forecast_14d_rainfall_mm": 11.0,
            "soil_moisture_pct": 16,
            "max_temp_c": 38.0,
            "dry_spell_days": 21,
            "drought_alert_level": "CRITICAL",
            "groundwater_status": "Over-Exploited",
            "forecast_daily": [
                {"day": "Day 1-7", "temp": "38°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry"},
                {"day": "Day 8-14", "temp": "37°C", "rain_prob": "10%", "icon": "☀️", "status": "Low Moisture"}
            ]
        }
    },
    "Andhra Pradesh": {
        "Anantapur": {
            "rainfall_deficit_pct": -58,
            "forecast_14d_rainfall_mm": 6.0,
            "soil_moisture_pct": 12,
            "max_temp_c": 39.5,
            "dry_spell_days": 27,
            "drought_alert_level": "CRITICAL",
            "groundwater_status": "Deep Water Table Depletion (>120m)",
            "forecast_daily": [
                {"day": "Day 1-5", "temp": "40°C", "rain_prob": "0%", "icon": "🔥", "status": "Acute Heat"},
                {"day": "Day 6-14", "temp": "38°C", "rain_prob": "5%", "icon": "☀️", "status": "Severe Aridity"}
            ]
        },
        "Kurnool": {
            "rainfall_deficit_pct": -45,
            "forecast_14d_rainfall_mm": 14.0,
            "soil_moisture_pct": 19,
            "max_temp_c": 38.2,
            "dry_spell_days": 18,
            "drought_alert_level": "SEVERE",
            "groundwater_status": "Semi-Critical",
            "forecast_daily": [
                {"day": "Day 1-7", "temp": "38°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry Spell"},
                {"day": "Day 8-14", "temp": "37°C", "rain_prob": "10%", "icon": "⛅", "status": "Dry"}
            ]
        }
    },
    "Maharashtra": {
        "Solapur": {
            "rainfall_deficit_pct": -49,
            "forecast_14d_rainfall_mm": 10.0,
            "soil_moisture_pct": 15,
            "max_temp_c": 38.6,
            "dry_spell_days": 22,
            "drought_alert_level": "CRITICAL",
            "groundwater_status": "Over-Exploited / Drought Prone",
            "forecast_daily": [
                {"day": "Day 1-7", "temp": "39°C", "rain_prob": "0%", "icon": "🔥", "status": "High Heat"},
                {"day": "Day 8-14", "temp": "37°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry Spell"}
            ]
        },
        "Ahmednagar": {
            "rainfall_deficit_pct": -42,
            "forecast_14d_rainfall_mm": 16.0,
            "soil_moisture_pct": 20,
            "max_temp_c": 37.0,
            "dry_spell_days": 17,
            "drought_alert_level": "SEVERE",
            "groundwater_status": "Semi-Critical",
            "forecast_daily": [
                {"day": "Day 1-7", "temp": "37°C", "rain_prob": "10%", "icon": "☀️", "status": "Dry"},
                {"day": "Day 8-14", "temp": "36°C", "rain_prob": "10%", "icon": "⛅", "status": "Dry"}
            ]
        }
    },
    "Karnataka": {
        "Kalaburagi": {
            "rainfall_deficit_pct": -47,
            "forecast_14d_rainfall_mm": 11.5,
            "soil_moisture_pct": 17,
            "max_temp_c": 38.4,
            "dry_spell_days": 20,
            "drought_alert_level": "CRITICAL",
            "groundwater_status": "Critical",
            "forecast_daily": [
                {"day": "Day 1-7", "temp": "38°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry"},
                {"day": "Day 8-14", "temp": "37°C", "rain_prob": "10%", "icon": "☀️", "status": "Dry"}
            ]
        }
    }
}

# Routine High-Water Crops Catalog
ROUTINE_CROPS_CATALOG: Dict[str, Dict[str, Any]] = {
    "Paddy": {
        "name": "Paddy / Rice",
        "water_mm": 1250,
        "liters_per_acre": 12500000,
        "cost_of_cultivation_per_acre": 26000,
        "pumping_power_cost_per_acre": 7500,
        "average_yield_qtl_per_acre": 24,
        "msp_per_quintal": 2320,
        "gross_income_per_acre": 55680,
        "net_income_per_acre": 22180,
        "risk_rating": "CRITICAL IN DRY SPELL",
        "water_intensity": "Very High (1,250 mm)"
    },
    "Sugarcane": {
        "name": "Sugarcane",
        "water_mm": 2100,
        "liters_per_acre": 21000000,
        "cost_of_cultivation_per_acre": 45000,
        "pumping_power_cost_per_acre": 14000,
        "average_yield_qtl_per_acre": 350,
        "msp_per_quintal": 340,
        "gross_income_per_acre": 119000,
        "net_income_per_acre": 60000,
        "risk_rating": "EXTREME WATER EXHAUSTION",
        "water_intensity": "Extreme (2,100 mm)"
    },
    "Cotton": {
        "name": "Cotton",
        "water_mm": 750,
        "liters_per_acre": 7500000,
        "cost_of_cultivation_per_acre": 24000,
        "pumping_power_cost_per_acre": 4800,
        "average_yield_qtl_per_acre": 8,
        "msp_per_quintal": 7121,
        "gross_income_per_acre": 56968,
        "net_income_per_acre": 28168,
        "risk_rating": "HIGH (Pest & Boll Drop Under Water Stress)",
        "water_intensity": "Moderate-High (750 mm)"
    },
    "Banana": {
        "name": "Banana",
        "water_mm": 1800,
        "liters_per_acre": 18000000,
        "cost_of_cultivation_per_acre": 60000,
        "pumping_power_cost_per_acre": 12000,
        "average_yield_qtl_per_acre": 250,
        "msp_per_quintal": 1400,
        "gross_income_per_acre": 350000,
        "net_income_per_acre": 278000,
        "risk_rating": "SEVERE (Immediate Fruit Stunting Without Drip)",
        "water_intensity": "Very High (1,800 mm)"
    },
    "Wheat": {
        "name": "Wheat",
        "water_mm": 550,
        "liters_per_acre": 5500000,
        "cost_of_cultivation_per_acre": 18000,
        "pumping_power_cost_per_acre": 3500,
        "average_yield_qtl_per_acre": 18,
        "msp_per_quintal": 2275,
        "gross_income_per_acre": 40950,
        "net_income_per_acre": 19450,
        "risk_rating": "MODERATE",
        "water_intensity": "Moderate (550 mm)"
    }
}

# Climate-Resilient Alternative Migration Crops
CROP_MIGRATIONS: List[Dict[str, Any]] = [
    {
        "crop_id": "ragi",
        "name": "Finger Millet (Ragi / Chodi)",
        "category": "Millets (Shree Anna)",
        "water_mm": 310,
        "water_saved_pct_vs_paddy": 75.2,
        "msp_per_quintal": 4290,
        "duration_days": 100,
        "cost_of_cultivation_per_acre": 11000,
        "yield_qtl_per_acre": 14,
        "diversification_bonus_per_acre": 7000,
        "soil_health": "High drought resilience; thrives in dry red soils; requires 60% less chemical fertilizer.",
        "recommended_varieties": "GPU-28, ML-365, Vakula, Sri Chaitanya",
        "buyer_body": "State Civil Supplies & PDS Procurement (100% MSP guaranteed)",
        "highlight_tag": "⭐ Top Climate Resilient Crop"
    },
    {
        "crop_id": "redgram",
        "name": "Red Gram / Pigeon Pea (Tur / Arhar)",
        "category": "Pulses",
        "water_mm": 400,
        "water_saved_pct_vs_paddy": 68.0,
        "msp_per_quintal": 7550,
        "duration_days": 140,
        "cost_of_cultivation_per_acre": 13500,
        "yield_qtl_per_acre": 7.5,
        "diversification_bonus_per_acre": 7000,
        "soil_health": "Deep taproot breaks hard soil pan; fixes 40 kg atmospheric Nitrogen/acre.",
        "recommended_varieties": "PRG-176, ICPL-87119 (Asha), BDN-711, WRG-65",
        "buyer_body": "NAFED & Central Pulse Buffer Procurement",
        "highlight_tag": "💰 Highest MSP Return"
    },
    {
        "crop_id": "groundnut",
        "name": "Groundnut (Peanut / Verusenaga)",
        "category": "Oilseeds",
        "water_mm": 500,
        "water_saved_pct_vs_paddy": 60.0,
        "msp_per_quintal": 6783,
        "duration_days": 105,
        "cost_of_cultivation_per_acre": 16000,
        "yield_qtl_per_acre": 10,
        "diversification_bonus_per_acre": 7000,
        "soil_health": "Excellent cash crop under drip; leaves nitrogen-rich biomass residue.",
        "recommended_varieties": "Kadiri-6, Kadiri-9, TG-37A, TAG-24, Dharani",
        "buyer_body": "MARKFED & Oilseeds Growers Federation",
        "highlight_tag": "🥜 Quick Cash Turnaround"
    },
    {
        "crop_id": "greengram",
        "name": "Greengram (Moong Dal)",
        "category": "Emergency Catch Pulses",
        "water_mm": 260,
        "water_saved_pct_vs_paddy": 79.2,
        "msp_per_quintal": 8682,
        "duration_days": 65,
        "cost_of_cultivation_per_acre": 8500,
        "yield_qtl_per_acre": 5.5,
        "diversification_bonus_per_acre": 7000,
        "soil_health": "Fastest harvest turnaround (65 days); minimal risk during acute dry spells.",
        "recommended_varieties": "WGG-42, IPM-02-3, MGG-348, Virat",
        "buyer_body": "NAFED e-Samridhi DBT portal",
        "highlight_tag": "⚡ 65-Day Drought Escape"
    },
    {
        "crop_id": "pearlmillet",
        "name": "Pearl Millet (Bajra / Sajja)",
        "category": "Millets (Shree Anna)",
        "water_mm": 290,
        "water_saved_pct_vs_paddy": 76.8,
        "msp_per_quintal": 2625,
        "duration_days": 85,
        "cost_of_cultivation_per_acre": 9000,
        "yield_qtl_per_acre": 16,
        "diversification_bonus_per_acre": 7000,
        "soil_health": "Survives temperature up to 44°C; very low water table requirement.",
        "recommended_varieties": "GHB-538, HHB-67 Improved, MPMH-17",
        "buyer_body": "Food Corporation of India (FCI) & State Millet Mission",
        "highlight_tag": "☀️ Extreme Heat Survivor"
    }
]

# State Nodal Micro-Irrigation Bodies
STATE_MICRO_IRRIGATION_BODIES: Dict[str, Dict[str, Any]] = {
    "Telangana": {
        "agency_name": "Telangana State Micro Irrigation Project (TSMIP)",
        "department": "Department of Horticulture & Agriculture, Govt of Telangana",
        "subsidy_sf_mf": 90,
        "subsidy_sc_st": 100,
        "subsidy_general": 80,
        "max_land_limit_acres": 12.5,
        "application_mode": "Online via MeeSeva & horticulture.tg.gov.in",
        "helpline": "040-23222222 / 1800-425-3502",
        "portal_url": "https://horticulture.tg.gov.in",
        "chc_rental_hub": "Custom Hiring Centers (CHCs) at Rythu Vedikas & PACS (Rental: ₹350/day)"
    },
    "Andhra Pradesh": {
        "agency_name": "Andhra Pradesh Micro Irrigation Project (APMIP)",
        "department": "Horticulture Department, Govt of Andhra Pradesh",
        "subsidy_sf_mf": 90,
        "subsidy_sc_st": 100,
        "subsidy_general": 70,
        "max_land_limit_acres": 12.5,
        "application_mode": "Online via Rythu Bharosa Kendrams (RBK) & apmip.ap.gov.in",
        "helpline": "155251 / 1800-425-3077",
        "portal_url": "https://apmip.ap.gov.in",
        "chc_rental_hub": "RBK Community Machinery Hiring Hubs (Rental: ₹400/day)"
    },
    "Maharashtra": {
        "agency_name": "MahaDBT Micro Irrigation Scheme (PMKSY-PDMC Top-up)",
        "department": "Commissioner of Agriculture, Maharashtra",
        "subsidy_sf_mf": 80,
        "subsidy_sc_st": 80,
        "subsidy_general": 75,
        "max_land_limit_acres": 12.5,
        "application_mode": "MahaDBT Farmer Portal (mahadbt.maharashtra.gov.in)",
        "helpline": "022-49150800",
        "portal_url": "https://mahadbt.maharashtra.gov.in",
        "chc_rental_hub": "Krishi Seva Kendra Equipment Banks (Rental: ₹450/day)"
    },
    "Karnataka": {
        "agency_name": "Krishi Bhagya & Micro Irrigation Project",
        "department": "Department of Agriculture, Govt of Karnataka",
        "subsidy_sf_mf": 75,
        "subsidy_sc_st": 90,
        "subsidy_general": 75,
        "max_land_limit_acres": 12.5,
        "application_mode": "K-Kisan Raitha Mitra Centers",
        "helpline": "080-22212804",
        "portal_url": "https://raitamitra.karnataka.gov.in",
        "chc_rental_hub": "Raitha Samparka Kendras (RSK) Rental Sets (Rental: ₹350/day)"
    },
    "Default": {
        "agency_name": "Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)",
        "department": "Department of Agriculture & Farmers Welfare, Ministry of Agriculture, Govt of India",
        "subsidy_sf_mf": 80,
        "subsidy_sc_st": 90,
        "subsidy_general": 55,
        "max_land_limit_acres": 12.5,
        "application_mode": "District Horticulture Office (DHO) / State Agriculture Portal",
        "helpline": "1800-180-1551 (Kisan Call Centre)",
        "portal_url": "https://pmksy.gov.in",
        "chc_rental_hub": "Sub-Mission on Agricultural Mechanization (SMAM) CHC Hubs (Rental: ₹400/day)"
    }
}


def generate_14day_forecast_strip(base_temp: float = 37.5, alert_level: str = "CRITICAL") -> List[Dict[str, Any]]:
    """Generates 14 distinct individual daily weather cards for horizontal agro-met forecast."""
    icons = ["☀️", "☀️", "☀️", "⛅", "🔥", "☀️", "🌦️", "☀️", "☀️", "🔥", "⛅", "☀️", "☀️", "☀️"]
    statuses = ["Severe Dry", "Sunny & Dry", "Dry Spell", "Partly Cloudy", "Heatwave Alert", "Clear Sky", "Light Rain", "Dry", "Dry", "Extreme Heat", "Mild Cloud", "Hot & Dry", "Dry", "Dry"]
    days_data = []
    
    for i in range(1, 15):
        temp = round(base_temp + ((i % 4) - 1.5) * 0.7, 1)
        if i == 7:
            rain = "15%"
            icon = "🌦️"
            status = "Light Rain"
        elif i in [4, 11]:
            rain = "10%"
            icon = "⛅"
            status = "Partly Cloudy"
        elif i in [5, 10]:
            rain = "0%"
            icon = "🔥"
            status = "Heatwave Alert"
        else:
            rain = "0%"
            icon = "☀️"
            status = "Zero Rain / Dry"
            
        days_data.append({
            "day": f"Day {i}",
            "temp": f"{temp}°C",
            "rain_prob": rain,
            "icon": icon,
            "status": status
        })
    return days_data

def get_district_weather(state: str, district: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves near-future weather forecast and drought stress for a district."""
    state_profiles = DISTRICT_WEATHER_PROFILES.get(state, {})
    if district and district in state_profiles:
        profile = state_profiles[district]
        profile["state"] = state
        profile["district"] = district
        profile = profile.copy()
        profile["forecast_daily"] = generate_14day_forecast_strip(profile.get("max_temp_c", 37.5), profile.get("drought_alert_level", "CRITICAL"))
        return profile
    
    # Return first available in state or default profile
    if state_profiles:
        first_dist = list(state_profiles.keys())[0]
        p = state_profiles[first_dist].copy()
        p["state"] = state
        p["district"] = first_dist
        return p
        
    # Generic fallback
    return {
        "state": state,
        "district": district or "District Capital",
        "rainfall_deficit_pct": -42,
        "forecast_14d_rainfall_mm": 15.0,
        "soil_moisture_pct": 20,
        "max_temp_c": 37.0,
        "dry_spell_days": 16,
        "drought_alert_level": "SEVERE",
        "groundwater_status": "Semi-Critical Deficit",
        "forecast_daily": [
            {"day": "Day 1-4", "temp": "37°C", "rain_prob": "5%", "icon": "☀️", "status": "Dry"},
            {"day": "Day 5-9", "temp": "38°C", "rain_prob": "0%", "icon": "☀️", "status": "Low Moisture"},
            {"day": "Day 10-14", "temp": "36°C", "rain_prob": "10%", "icon": "⛅", "status": "Partly Dry"}
        ]
    }

def compute_agro_climate_ecosystem(
    state: str = "Telangana",
    district: Optional[str] = "Warangal",
    routine_crop: str = "Paddy",
    irrigation_type: str = "flood",
    acres: float = 2.5,
    farmer_category: str = "small_marginal"
) -> Dict[str, Any]:
    """
    Computes complete advisory ecosystem:
    1. Near-future weather forecast & drought warning.
    2. Need for Drip Irrigation: Buy vs Rent subsidy computation.
    3. Crop Migration matrix with water savings and financials.
    """
    weather = get_district_weather(state, district)
    
    # Check if routine crop exists
    norm_crop = "Paddy"
    for k in ROUTINE_CROPS_CATALOG:
        if k.lower() in routine_crop.lower():
            norm_crop = k
            break
            
    crop_info = ROUTINE_CROPS_CATALOG.get(norm_crop, ROUTINE_CROPS_CATALOG["Paddy"])
    
    # Check Irrigation status
    irrigation_norm = irrigation_type.lower()
    has_drip = "drip" in irrigation_norm or "micro" in irrigation_norm or "sprinkler" in irrigation_norm
    
    # Determine Drip Subsidy Profile
    agency_info = STATE_MICRO_IRRIGATION_BODIES.get(state, STATE_MICRO_IRRIGATION_BODIES["Default"])
    
    cat_lower = farmer_category.lower()
    if "sc" in cat_lower or "st" in cat_lower:
        subsidy_pct = agency_info["subsidy_sc_st"]
    elif "small" in cat_lower or "marginal" in cat_lower or acres <= 5.0:
        subsidy_pct = agency_info["subsidy_sf_mf"]
    else:
        subsidy_pct = agency_info["subsidy_general"]
        
    market_rate_per_acre = 32000
    total_drip_market_cost = round(acres * market_rate_per_acre, 2)
    subsidy_amount = round(total_drip_market_cost * (subsidy_pct / 100.0), 2)
    farmer_share = round(total_drip_market_cost - subsidy_amount, 2)
    
    # Micro Irrigation Recommendation block
    drip_advisory = {
        "has_drip": has_drip,
        "is_drip_urgently_needed": not has_drip and weather["rainfall_deficit_pct"] <= -20,
        "urgency_level": "CRITICAL IMMEDIATE ACTION" if not has_drip and weather["rainfall_deficit_pct"] <= -40 else "HIGH RECOMMENDED",
        "agency_name": agency_info["agency_name"],
        "department": agency_info["department"],
        "subsidy_percentage": subsidy_pct,
        "total_market_cost": total_drip_market_cost,
        "government_subsidy_amount": subsidy_amount,
        "farmer_payable_share": farmer_share,
        "application_mode": agency_info["application_mode"],
        "helpline": agency_info["helpline"],
        "portal_url": agency_info["portal_url"],
        "rent_option": {
            "title": "Subsidized Rental from Custom Hiring Center (CHC)",
            "chc_provider": agency_info["chc_rental_hub"],
            "rental_rate_per_day": "₹350 - ₹450 / day",
            "advantage": "Zero upfront capital, immediate deployment for next 15-20 critical dry days."
        }
    }
    
    # Crop Migrations Calculation
    routine_water_total = crop_info["water_mm"]
    routine_liters_total = round(crop_info["liters_per_acre"] * acres)
    routine_net_total = round(crop_info["net_income_per_acre"] * acres)
    
    migrations = []
    for m in CROP_MIGRATIONS:
        water_saved_pct = round(((routine_water_total - m["water_mm"]) / routine_water_total) * 100, 1)
        liters_saved = round((routine_water_total - m["water_mm"]) * 10000 * acres)
        
        # Calculate gross and net returns with diversification bonus
        gross_per_acre = m["yield_qtl_per_acre"] * m["msp_per_quintal"]
        net_per_acre = gross_per_acre - m["cost_of_cultivation_per_acre"] + m["diversification_bonus_per_acre"]
        total_net_for_acres = round(net_per_acre * acres)
        profit_diff = total_net_for_acres - routine_net_total
        
        migrations.append({
            "crop_id": m["crop_id"],
            "name": m["name"],
            "category": m["category"],
            "water_required_mm": m["water_mm"],
            "water_saved_pct": water_saved_pct,
            "liters_saved_total": liters_saved,
            "msp_per_quintal": m["msp_per_quintal"],
            "duration_days": m["duration_days"],
            "days_saved_vs_routine": max(0, 140 - m["duration_days"]),
            "diversification_bonus_per_acre": m["diversification_bonus_per_acre"],
            "net_income_per_acre": net_per_acre,
            "total_net_income": total_net_for_acres,
            "net_profit_difference": profit_diff,
            "soil_health": m["soil_health"],
            "recommended_varieties": m["recommended_varieties"],
            "buyer_body": m["buyer_body"],
            "highlight_tag": m["highlight_tag"]
        })
        
    return {
        "status": "success",
        "location": {
            "state": state,
            "district": weather["district"]
        },
        "weather": weather,
        "routine_crop": {
            "crop_name": crop_info["name"],
            "water_mm": crop_info["water_mm"],
            "water_intensity": crop_info["water_intensity"],
            "risk_rating": crop_info["risk_rating"],
            "total_water_liters": routine_liters_total,
            "pumping_power_cost": round(crop_info["pumping_power_cost_per_acre"] * acres),
            "net_income_total": routine_net_total
        },
        "micro_irrigation_advisory": drip_advisory,
        "crop_migrations": migrations
    }
