import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AstroPredictor Premium"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # PDF Settings
    PDF_OUTPUT_DIR: str = "generated_reports"

    class Config:
        env_file = ".env"

settings = Settings()
