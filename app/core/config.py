from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API
    api_title: str = "Clínica Pediátrica API"
    api_version: str = "1.0.0"
    api_description: str = "Sistema moderno para gestión de clínica pediátrica"
    debug: bool = True
    
    # Database
    database_url: str
    supabase_url: str
    supabase_key: str
    
    # Seguridad
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración cacheada"""
    return Settings()
