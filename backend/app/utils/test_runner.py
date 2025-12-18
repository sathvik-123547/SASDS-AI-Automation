import subprocess
from fastapi import HTTPException

def run_tests_in_project(project_path: str) -> tuple:
    """
    Runs pytest inside the generated project folder.
    Returns:
      (success: bool, output: str)
    """

    try:
        # Run pytest in the generated project folder
        result = subprocess.run(
            ["pytest", "-q"],  # quiet mode
            cwd=project_path,  # run inside generated folder
            text=True,
            capture_output=True
        )

        success = result.returncode == 0
        output = result.stdout + "\n" + result.stderr

        return success, output

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="pytest is not installed or not available in PATH."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running tests: {str(e)}"
        )
