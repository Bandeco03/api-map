import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # API Configuration
    API_ACCESS_KEY: str = os.getenv("API_ACCESS_KEY")
    API_TOKEN: str = os.getenv("API_TOKEN")
    API_APPKEY: str = os.getenv("API_APPKEY")
    
    # Database Configuration (for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./api_map.db")
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")


settings = Settings()
