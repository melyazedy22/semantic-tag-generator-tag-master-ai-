"""config.py — loads settings from .env or Azure environment variables"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # SECURITY: No default value — key MUST be provided via environment variable
    # Locally: set in .env file
    # On Azure: set as a Container App environment variable (never in code!)
    groq_api_key: str
    groq_model:   str = "llama-3.1-8b-instant"
    max_tags:     int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
