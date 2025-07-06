from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Issues & Insights Tracker"
    
    # Use SQLite for development (easier setup)
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./tracker.db"
    
    # PostgreSQL settings (for production)
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "281003"
    POSTGRES_DB: str = "tracker"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    class Config:
        case_sensitive = True

settings = Settings()
