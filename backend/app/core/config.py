import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file if available

class Settings:
    PROJECT_NAME: str = "TOEFL Chatbot Backend"
    API_V1_STR: str = "/api/v1"
    DB_URL: str = os.getenv("DB_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    ALGORITHM: str = "HS256"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "dummy")
    GEMINI_API_URL: str = os.getenv("GEMINI_API_URL", "https://api.gemini.google.com/v1/chat/completions")

settings = Settings()