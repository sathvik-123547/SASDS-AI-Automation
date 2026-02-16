from app.core.config import settings
from fastapi import HTTPException
import google.generativeai as genai

# Configure Gemini once at import time
if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=settings.GEMINI_API_KEY)

# You can switch models here if needed
GEMINI_MODEL_NAME = settings.GEMINI_MODEL_NAME  # or another supported model


def analyze_requirements_with_gemini(requirements_text: str) -> dict:
    """
    Sends the user requirements text to Gemini and expects a strictly JSON response
    that we will parse into our RequirementAnalysisResponse model.
    """
    if not requirements_text.strip():
        raise HTTPException(
            status_code=400,
            detail="requirements_text cannot be empty."
        )
    prompt = f"""
You are an expert software architect. 
Your ONLY task is to analyze the user's natural language software requirements 
and return a STRICT JSON object.

⚠️ RULES (IMPORTANT):
- Respond with ONLY valid JSON. No explanations.
- No backticks, no markdown, no comments.
- Do not add extra text before or after the JSON.
- Keep all keys exactly as specified.

Return JSON in this exact structure:

{{
  "modules": [
    {{ "name": "string", "description": "string" }}
  ],
  "entities": [
    {{ "name": "string", "attributes": ["string"] }}
  ],
  "apis": [
    {{ "name": "string", "method": "GET", "path": "/api/example", "description": "string" }}
  ],
  "non_functional_requirements": ["string"],
  "tech_stack_suggestions": ["string"],
  "missing_information": ["string"]
}}

Now analyze the user's requirements and fill the structure.

USER REQUIREMENTS:
\"\"\"{requirements_text}\"\"\"
""".strip()

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        import json
        parsed = json.loads(raw_text)
        return parsed

    except Exception as e:
        # You might want more granular error handling/logging here
        raise HTTPException(status_code=500, detail=f"Gemini analysis failed: {str(e)}")
