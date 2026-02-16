from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    """
    PROJECT_NAME: str = "Task Manager API"
    API_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite+aiosqlite:///./task_manager.db" # Default for local SQLite

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
