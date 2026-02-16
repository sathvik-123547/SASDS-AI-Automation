from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """
    DATABASE_URL: str = "sqlite:///./test.db" # Default for tests, overridden by .env in production

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        extra='ignore' # Ignore extra fields not defined here
    )

settings = Settings()
