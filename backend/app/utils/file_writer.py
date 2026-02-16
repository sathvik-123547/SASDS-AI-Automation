import os


BASE_DIR = os.path.abspath("generated_projects")

def write_generated_files(project_id: str, files: list) -> str:
    """
    Writes generated files to disk under:
    generated_projects/{project_id}/

    Each file entry is expected to have:
    - path: file path relative to project root
    - content: string (file content)
    - description: optional description

    Returns: absolute path of generated project folder
    """

    base_dir = os.path.abspath("generated_projects")
    project_dir = os.path.join(base_dir, project_id)

    # Ensure base and project directories exist
    os.makedirs(project_dir, exist_ok=True)

    for file in files:
        rel_path = file["path"]
        content = file["content"]

        # Full path e.g. generated_projects/project_001/backend/app/main.py
        full_path = os.path.join(project_dir, rel_path)

        # Create directory path if needed
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write file content
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    return project_dir
