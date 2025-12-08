from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # You can add more config options later:
    # DEFAULT_MODEL: str = "gemini-1.5-flash"

settings = Settings()
