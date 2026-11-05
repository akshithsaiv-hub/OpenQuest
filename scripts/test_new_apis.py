import urllib.request
import json

base_url = "http://127.0.0.1:8000"

# 1. Test Document Downloads
doc_types = ["aadhaar", "pahani", "ccrc", "passbook"]
for dt in doc_types:
    url = f"{base_url}/api/documents/download/{dt}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        status = resp.status
        cd = resp.headers.get("Content-Disposition")
        ct = resp.headers.get("Content-Type")
        body = resp.read()
        print(f"Doc {dt}: Status={status}, Content-Type={ct}, Disposition={cd}, Size={len(body)} bytes")
        assert status == 200
        assert "<svg" in body.decode("utf-8")

# 2. Test Voice Assistant
queries = [
    {"query": "Drip irrigation subsidy in Telangana", "language": "te-IN"},
    {"query": "KCC loan interest rate", "language": "hi-IN"},
    {"query": "How to report crop loss within 72 hours under PMFBY?", "language": "en-IN"}
]

for q in queries:
    req = urllib.request.Request(
        f"{base_url}/api/voice_assistant",
        data=json.dumps(q).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        lang_ascii = res.get("language_name", "").encode("ascii", "replace").decode("ascii")
        print(f"Voice query test: Lang={lang_ascii}, Code={res.get('tts_code')}, Status={res.get('status')}")
        assert res.get("status") == "success"
        assert len(res.get("response_text", "")) > 10

print("\nALL BACKEND API VERIFICATIONS PASSED SUCCESSFULLY!")
