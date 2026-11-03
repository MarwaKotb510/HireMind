# probe.py
from google import genai
from google.genai import errors
from app.config import get_settings

s = get_settings()
client = genai.Client(api_key=s.gemini_api_key)

for model in [s.gemini_model, "gemini-2.5-flash", "gemini-3.1-flash-lite"]:
    try:
        r = client.models.generate_content(model=model, contents="Say hello in Arabic.")
        print(model, "-> OK:", (r.text or "")[:60])
    except errors.APIError as e:
        print(model, "-> ERROR code:", getattr(e, "code", None), "|", str(e)[:150])
    except Exception as e:
        print(model, "-> UNEXPECTED:", type(e).__name__)