import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

models = genai.list_models()
for m in models:
    print(m.name)
