import json
import google.generativeai as genai
from fastapi import HTTPException
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
MODEL = "models/gemini-2.5-flash"


def generate_tests(requirements_text: str, files: list) -> dict:
    """
    Uses Gemini to generate unit test files based on generated project code.
    Returns a dict matching TestGenerationResponse.
    """

    if not requirements_text.strip():
        raise HTTPException(status_code=400, detail="requirements_text cannot be empty.")

    if not files:
        raise HTTPException(status_code=400, detail="files must contain generated code.")

    # Convert code files to clean JSON string
    file_list_str = json.dumps(files, indent=2)

    prompt = f"""
You are an expert Python QA engineer.

Your task:
- Read the project requirements.
- Read the generated project source code.
- Create Python **unit tests** using pytest.

Rules:
- Output ONLY JSON.
- Structure:
{{
  "tests": [
    {{
      "path": "tests/test_tasks.py",
      "content": "pytest compatible code"
    }}
  ]
}}

Guidelines:
- Tests must be runnable immediately.
- Import the actual modules based on the given paths.
- Name test files under a `tests/` folder.
- Include tests for:
  - Success cases
  - Failure cases
  - Edge cases

REQUIREMENTS:
\"\"\"{requirements_text}\"\"\"

SOURCE FILES:
\"\"\"{file_list_str}\"\"\"
    """.strip()

    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json"
            }
        )
        return json.loads(response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")
