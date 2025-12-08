import json
import google.generativeai as genai
from fastapi import HTTPException
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
MODEL = "models/gemini-2.5-flash"

def generate_fix(file_path: str, file_content: str, test_output: str) -> str:
    """
    Gemini analyzes the failing tests and returns a FIXED version of the code file.
    Returns the corrected file content as a string.
    """

    prompt = f"""
You are an expert Python software engineer.

You are given:
1. A code file that contains bugs.
2. The failing pytest output (errors + stack traces).

Your task:
- Analyze what caused the test to fail.
- FIX the code.
- Return ONLY the corrected file content.
- DO NOT output explanations.
- DO NOT return JSON.
- Return ONLY the raw corrected Python code.

File Path:
{file_path}

Original File Content:
\"\"\"
{file_content}
\"\"\"

Failing Test Output:
\"\"\"
{test_output}
\"\"\"
"""

    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "text/plain"
            }
        )
        return response.text

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini fix generation failed: {str(e)}"
        )
