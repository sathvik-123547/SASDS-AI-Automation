import os
from app.utils.test_runner import run_tests_in_project
from app.services.fix_generator import generate_fix

def run_self_correction(project_path: str, max_attempts: int = 3):
    """
    Attempts to fix failing tests automatically using Gemini.
    Returns final status and output logs.
    """

    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}: Running tests...")

        success, output = run_tests_in_project(project_path)

        if success:
            return {
                "success": True,
                "attempts": attempt,
                "message": "All tests passed successfully.",
                "logs": output
            }

        # If tests failed:
        print("Tests failed, sending to Gemini for fixing...")

        failing_output = output

        # Detect failing file (pytest always shows file paths)
        failing_file = None
        for line in failing_output.split("\n"):
            if line.strip().endswith(".py") and os.path.exists(os.path.join(project_path, line.strip())):
                failing_file = line.strip()
                break

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
