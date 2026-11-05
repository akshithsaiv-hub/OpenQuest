import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_path = os.path.join(base_dir, 'backend', 'eligibility_api.py')

with open(backend_path, 'r', encoding='utf-8') as f:
    code = f.read()

snippet = """
class VoiceQueryRequest(BaseModel):
    query: str
    language: Optional[str] = "auto"

@app.post("/api/voice_assistant")
def api_voice_assistant(req: VoiceQueryRequest):
    \"\"\"
    Multilingual voice assistant endpoint understanding and responding in any major Indian language.
    \"\"\"
    from utils.voice_engine import get_voice_response
    return get_voice_response(query=req.query, lang_code=req.language or "auto")

@app.get("/api/documents/download/{doc_type}")
def api_download_sample_document(doc_type: str):
    \"\"\"
    Serves downloadable official sample document copies for Aadhaar, Pahani, Passbook, and CCRC.
    \"\"\"
    samples_dir = os.path.join(FRONTEND_DIR, "samples")
    doc_map = {
        "aadhaar": ("sample_aadhaar.svg", "Sample_Aadhaar_Card_Masked.svg"),
        "pahani": ("sample_pahani.svg", "Sample_Pahani_Land_Record_RoR1B.svg"),
        "land_record": ("sample_pahani.svg", "Sample_Pahani_Land_Record_RoR1B.svg"),
        "passbook": ("sample_passbook.svg", "Sample_Bank_Passbook_DBT_Active.svg"),
        "bank_passbook": ("sample_passbook.svg", "Sample_Bank_Passbook_DBT_Active.svg"),
        "ccrc": ("sample_ccrc.svg", "Sample_CCRC_Tenant_Card.svg"),
        "ccrc_tenancy": ("sample_ccrc.svg", "Sample_CCRC_Tenant_Card.svg")
    }
    key = doc_type.lower().strip()
    if key not in doc_map:
        raise HTTPException(status_code=404, detail=f"Document type '{doc_type}' not found.")
    file_name, download_name = doc_map[key]
    file_path = os.path.join(samples_dir, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample file not found on server")
    return FileResponse(
        path=file_path,
        filename=download_name,
        media_type="image/svg+xml",
        headers={"Content-Disposition": f'attachment; filename="{download_name}"'}
    )
"""

target = '# Mount static files to serve the frontend portal'
if target in code and '/api/voice_assistant' not in code:
    new_code = code.replace(target, snippet.strip() + '\n\n' + target)
    with open(backend_path, 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Backend routes patched successfully!")
else:
    print("Already patched or target not found.")
