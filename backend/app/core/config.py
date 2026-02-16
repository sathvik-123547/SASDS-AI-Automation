import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Metadata storage
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./metadata.sqlite")

    # GitHub sync (optional)
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_REPO: str = os.getenv("GITHUB_REPO", "")  # e.g. "owner/repo"
    GITHUB_BRANCH: str = os.getenv("GITHUB_BRANCH", "main")

    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "models/gemini-2.5-flash")


settings = Settings()
