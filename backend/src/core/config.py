from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    QDRANT_URL: str
    QDRANT_API_KEY: str
    NEON_DATABASE_URL: str

    # Qdrant Collection Name
    QDRANT_COLLECTION_NAME: str = "giaic-q4-hackathon"

    # App settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RAG Chatbot API"

    # Authentication settings
    BETTER_AUTH_SECRET: str = "tFl6eCnPw0MIHwMZaOJEvLLNIixnDVdZ"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_DAYS: int = 7

    # Rate limits for transformations
    TRANSFORM_RATE_LIMIT: int = 10
    TRANSFORM_RATE_WINDOW: int = 3600  # seconds

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()