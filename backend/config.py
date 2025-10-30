import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # API Configuration
    API_ACCESS_KEY: str = os.getenv("API_ACCESS_KEY", "3g1nrc7c59kxygt2i7idana49jpvw01f")
    API_SYS_CODE: str = os.getenv("API_SYS_CODE", "901")
    API_TOKEN: str = os.getenv("API_TOKEN", "110295_b1f25dda84f640c7acc6456bbbec9a47")
    API_APPKEY: str = os.getenv("API_APPKEY", "664780B4B466AB6F19DF393D5055D977")
    
    # Database Configuration (for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./api_map.db")
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")


settings = Settings()
