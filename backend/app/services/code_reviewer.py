import json

import google.generativeai as genai
from fastapi import HTTPException

from app.core.config import settings

if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = settings.GEMINI_MODEL_NAME


from typing import Optional

def review_code(requirements_text: Optional[str], files: list) -> dict:
    """
    Use Gemini to review a set of files and produce structured issues.
    Returns a dict matching CodeReviewResponse.
    """
    if not files:
        raise HTTPException(status_code=400, detail="files must not be empty.")

    file_list_str = json.dumps(files, indent=2)
    req_text = requirements_text or "No explicit requirements provided."

    prompt = f"""
You are a senior Python/FastAPI reviewer. Review the provided code against:
- readability and maintainability
- correctness and edge cases
- security and data validation
- performance and resource usage
- PEP-8 and common best practices

Return STRICT JSON, no markdown, in this exact structure:
{{
  "summary": "overall summary",
  "issues": [
    {{
      "severity": "info|low|medium|high|critical",
      "file": "path or null",
      "line": 123,
      "summary": "short description",
      "recommendation": "actionable fix"
    }}
  ]
}}

CONTEXT - REQUIREMENTS:
\"\"\"{req_text}\"\"\"

FILES (path, optional description, content):
\"\"\"{file_list_str}\"\"\"
""".strip()

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )
        raw = (response.text or "").strip()
        if not raw:
            raise HTTPException(
                status_code=500,
                detail="Gemini returned empty review response.",
            )
        data = json.loads(raw)
        if "summary" not in data or "issues" not in data:
            raise HTTPException(
                status_code=500,
                detail="Review JSON missing required keys.",
            )
        return data
    except HTTPException:
        raise
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini returned invalid JSON: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini review failed: {str(e)}",
        )


