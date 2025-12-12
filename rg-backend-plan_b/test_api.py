import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)

try:
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content("Say hello")
    print("✓ API Key is valid!")
    print(f"Response: {response.text[:50]}...")
except Exception as e:
    print(f"✗ API Key test failed: {e}")
