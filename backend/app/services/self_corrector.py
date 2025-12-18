import os
import re
from app.utils.test_runner import run_tests_in_project
from app.services.fix_generator import generate_fix


def _detect_failing_file(output: str, project_path: str) -> str | None:
    """
    Parse pytest output to find the first failing file that actually exists on disk.
    Accepts lines like:
      - tests/test_sample.py:12: AssertionError
      - E   File "/abs/path/tests/test_sample.py", line 12
    """
    for line in output.splitlines():
        match = re.search(r"([^\s:]+\\.py)(?::\\d+)?", line)
        if not match:
            continue

        candidate = match.group(1)
        # Handle absolute vs relative paths
        candidate_path = candidate
        if not os.path.isabs(candidate_path):
            candidate_path = os.path.join(project_path, candidate)

        candidate_path = os.path.normpath(candidate_path)

        if os.path.exists(candidate_path):
            # return relative path to keep downstream behavior the same
            return os.path.relpath(candidate_path, project_path)

    return None

def run_self_correction(project_path: str, max_attempts: int = 3):
    """
    Attempts to fix failing tests automatically using Gemini.
    Returns final status and output logs.
    """

    failing_output = ""

    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}: Running tests...")

        success, output = run_tests_in_project(project_path)
        failing_output = output

        if success:
            return {
                "success": True,
                "attempts": attempt,
                "message": "All tests passed successfully.",
                "logs": output
            }

        # If tests failed:
        print("Tests failed, sending to Gemini for fixing...")

        failing_file = _detect_failing_file(failing_output, project_path)

        if not failing_file:
            return {
                "success": False,
                "attempts": attempt,
                "message": "Could not detect failing file.",
                "logs": failing_output
            }

        # Load failing file
        full_path = os.path.join(project_path, failing_file)
        with open(full_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        # Ask Gemini to fix it
        fixed_content = generate_fix(failing_file, original_content, failing_output)

        # Write updated file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(fixed_content)

    return {
        "success": False,
        "attempts": max_attempts,
        "message": "Max attempts reached. Tests still failing.",
        "logs": failing_output
    }
