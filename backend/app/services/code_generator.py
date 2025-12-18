import json
import re

import google.generativeai as genai
from fastapi import HTTPException

from app.core.config import settings

# Configure Gemini
if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=settings.GEMINI_API_KEY)

GEMINI_MODEL_NAME = "models/gemini-2.5-flash"


def generate_code_with_gemini(requirements_text: str, analysis: dict | None = None) -> dict:
    """
    Uses Gemini to generate a set of files (path + content) for the project.
    Returns a dict that matches CodeGenerationResponse.

    We enforce JSON output using response_mime_type='application/json'
    so that response.text is guaranteed to be JSON.
    """
    if not requirements_text.strip():
        raise HTTPException(
            status_code=400,
            detail="requirements_text cannot be empty."
        )

    # Build analysis text (optional)
    analysis_str = json.dumps(analysis, indent=2) if analysis else "null"

    prompt = f"""
You are an expert software engineer and software architect.

You will receive:
1. A natural language description of a software project.
2. An optional structured requirements analysis object (may be null).

Your job is to design a CLEAN, MODULAR Python backend project and return
ONLY a JSON object describing the generated files.

The JSON MUST have this exact structure:

{{
  "files": [
    {{
      "path": "string, e.g. backend/app/main.py or backend/app/api/users.py",
      "description": "short human description of what this file does",
      "content": "FULL file content as a string (valid Python code, no placeholders)"
    }}
  ]
}}

Rules:
- Respond with STRICTLY valid JSON.
- No markdown, no backticks, no extra commentary.
- "files" must be a non-empty array.
- "path" should be relative to the project root, using forward slashes.
- Prefer a FastAPI + Python service architecture.
- Focus on a minimal but working MVP, not perfection.
- At this stage, DO NOT include tests or CI files; only application code.

Here is the user requirements text:

\"\"\"{requirements_text}\"\"\"

Here is the structured analysis (may be null):

\"\"\"{analysis_str}\"\"\"
    """.strip()

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)

        # 🔑 This forces the model to return proper JSON
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json"
            },
        )

        raw_text = (response.text or "").strip()
        if not raw_text:
            raise HTTPException(
                status_code=500,
                detail="Gemini returned an empty response for code generation.",
            )

        data = json.loads(raw_text)

        # Basic validation
        if "files" not in data or not isinstance(data["files"], list):
            raise HTTPException(
                status_code=500,
                detail="Gemini JSON output is missing 'files' array.",
            )

        return data

    except HTTPException:
        # bubble up known HTTP errors
        raise
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini returned invalid JSON: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini code generation failed: {str(e)}",
        )