import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_path = os.path.join(base_dir, "backend", "eligibility_api.py")

with open(api_path, "r", encoding="utf-8") as f:
    code = f.read()

new_routes = """class WeatherAdvisoryRequest(BaseModel):
    state: Optional[str] = "Telangana"
    district: Optional[str] = "Warangal"
    routine_crop: Optional[str] = "Paddy"
    irrigation_type: Optional[str] = "flood"
    acres: Optional[float] = 2.5
    farmer_category: Optional[str] = "small_marginal"

@app.post("/api/weather_advisory")
def api_weather_advisory(req: WeatherAdvisoryRequest):
    \"\"\"
    Agro-climatic intelligence endpoint:
    Evaluates near-future weather dry spells, matches Drip Subsidies (Buy vs Rent),
    and calculates routine crop migration options.
    \"\"\"
    from utils.agro_climate_advisory import compute_agro_climate_ecosystem
    return compute_agro_climate_ecosystem(
        state=req.state or "Telangana",
        district=req.district or "Warangal",
        routine_crop=req.routine_crop or "Paddy",
        irrigation_type=req.irrigation_type or "flood",
        acres=req.acres or 2.5,
        farmer_category=req.farmer_category or "small_marginal"
    )

@app.get("/api/weather_advisory")
def api_weather_advisory_get(
    state: str = "Telangana",
    district: Optional[str] = None,
    routine_crop: str = "Paddy",
    irrigation_type: str = "flood",
    acres: float = 2.5,
    farmer_category: str = "small_marginal"
):
    from utils.agro_climate_advisory import compute_agro_climate_ecosystem
    return compute_agro_climate_ecosystem(
        state=state,
        district=district,
        routine_crop=routine_crop,
        irrigation_type=irrigation_type,
        acres=acres,
        farmer_category=farmer_category
    )

@app.get("/api/weather_districts/{state}")
def api_get_weather_districts(state: str):
    from utils.agro_climate_advisory import DISTRICT_WEATHER_PROFILES
    districts = list(DISTRICT_WEATHER_PROFILES.get(state, {}).keys())
    if not districts:
        districts = ["District Capital / General"]
    return {"state": state, "districts": districts}
"""

marker = "# Mount static files to serve the frontend portal"
if marker in code and "/api/weather_advisory" not in code:
    code = code.replace(marker, new_routes + "\n" + marker)
    with open(api_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("backend/eligibility_api.py patched with weather advisory routes!")
else:
    print("Already patched or marker not found.")
