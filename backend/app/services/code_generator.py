import json
import re

import google.generativeai as genai
from fastapi import HTTPException

from app.core.config import settings

# Configure Gemini
if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=settings.GEMINI_API_KEY)

GEMINI_MODEL_NAME = settings.GEMINI_MODEL_NAME


from typing import Optional

def generate_code_with_gemini(requirements_text: str, analysis: Optional[dict] = None) -> dict:
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


def refine_code_with_gemini(path: str, content: str, instructions: str) -> dict:
    """
    Uses Gemini to refine specific file content based on instructions.
    """
    prompt = f"""
You are an expert software engineer.
You are asked to MODIFY an existing file based on specific instructions.

File Path: {path}

Current Content:
```python
{content}
```

Instructions:
"{instructions}"

Return ONLY valid JSON with this structure:
{{
  "path": "{path}",
  "new_content": "The FULL updated file content",
  "explanation": "A brief explanation of changes"
}}
""".strip()

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )
        
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refinement failed: {str(e)}")


def generate_code_with_gemini_stream(requirements_text: str, analysis: Optional[dict] = None):
    """
    Generator that yields chunks of text from Gemini for real-time streaming.
    Uses a special prompt format with delimiters.
    """
    analysis_str = json.dumps(analysis, indent=2) if analysis else "null"
    
    prompt = f"""
You are an expert software engineer.
Design a CLEAN, MODULAR Python backend project based on the following requirements.

Requirements:
{requirements_text}

Analysis:
{analysis_str}

Output the files one by one using this EXACT format:

### FILE: path/to/file.py
<file content here>
### END FILE ###

Rules:
- NO markdown code blocks (```python ... ```).
- NO JSON.
- Just plain text with the delimiters above.
- Ensure all files needed for a working MVP are included.
- "path" should be relative to project root.
    """.strip()

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        # We assume the model respects the text format. 
        # stream=True returns an iterator of chunks.
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"ERROR: {str(e)}"