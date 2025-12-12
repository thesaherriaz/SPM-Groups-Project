from app.config import settings

print(f"API Key loaded: {settings.gemini_api_key[:10]}..." if settings.gemini_api_key else "No API key")
print(f"Database URL loaded: {settings.database_url[:20]}..." if settings.database_url else "No DB URL")
print(f"API Key length: {len(settings.gemini_api_key)}")
