from google import genai

from app.config import get_settings

settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)

print("Configured model:", settings.gemini_model)
for model in client.models.list():
    if "gemini" in (model.name or ""):
        print(model.name)