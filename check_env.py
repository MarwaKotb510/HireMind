from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GEMINI_API_KEY") or ""
print("Length:", len(key))
print("Starts with 'AIza':", key.startswith("AIza"))
print("Contains space:", " " in key)
print("Contains quote:", '"' in key or "'" in key)
print("Contains '=':", "=" in key)