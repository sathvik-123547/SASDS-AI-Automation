from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Use SQLite for simplicity in MVP. For production, consider PostgreSQL.
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()