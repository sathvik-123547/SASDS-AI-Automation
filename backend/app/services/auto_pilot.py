import os
import json
import google.generativeai as genai
from typing import List, Dict, Any
from app.core.config import settings
from app.utils.file_writer import BASE_DIR

# Configure Gemini if not already done in main
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

GEMINI_MODEL_NAME = settings.GEMINI_MODEL_NAME

def analyze_project_structure(project_id: str) -> Dict[str, Any]:
    """
    Reads the project files and sends them to Gemini for analysis.
    """
    project_path = os.path.join(BASE_DIR, project_id)
    if not os.path.exists(project_path):
        return {"error": "Project not found"}

    # Read files
    files_content = {}
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.tsx', '.html', '.css', '.md', '.json')):
                # Skip venv, node_modules, .git
                if 'node_modules' in root or '.venv' in root or '.git' in root or '__pycache__' in root:
                    continue
                
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, project_path)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Limit file size to avoid token limits
                        if len(content) < 50000:
                            files_content[rel_path] = content
                        else:
                            files_content[rel_path] = "<file too large>"
                except Exception:
                    pass

    # Construct prompt
    prompt = f"""
You are an expert software architect and code reviewer.
Analyze the following project files and identify:
1. Potential bugs or logic errors.
2. Security vulnerabilities.
3. Code quality improvements (refactoring).
4. Missing features or best practices.

Project Files:
"""
    for path, content in files_content.items():
        prompt += f"\n--- FILE: {path} ---\n{content}\n"

    prompt += """
Return the analysis as a JSON object with this structure:
{
  "summary": "High-level summary of the project state.",
  "issues": [
    {
      "severity": "high" | "medium" | "low",
      "file": "path/to/file",
      "line": integer (optional),
      "description": "Description of the issue",
      "suggestion": "How to fix it"
    }
  ],
  "improvements": [
    {
      "type": "refactor" | "feature" | "security",
      "description": "Description",
      "file": "path/to/file (optional)"
    }
  ]
}
Respond with ONLY valid JSON.
"""

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
