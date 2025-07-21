from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    app_name: str = "MindCare"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server
    host: str = "localhost"
    port: int = 8000
    reload: bool = True
    
    # Base de données
    database_url: str = "sqlite:///./mindcare.db"
    
    # Sécurité
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Internationalisation
    default_language: str = "fr"
    supported_languages: List[str] = ["fr", "en", "ar"]
    
    # Thème
    default_theme: str = "light"
    supported_themes: List[str] = ["light", "dark"]
    
    # Chemins
    base_dir: Path = Path(__file__).parent.parent
    static_dir: Path = base_dir / "static"
    locales_dir: Path = base_dir / "locales"
    data_dir: Path = base_dir / "data"
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # Pagination
    default_page_size: int = 10
    max_page_size: int = 100
    
    # Upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx"]
    
    # Email (pour futures fonctionnalités)
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Cache
    cache_ttl: int = 3600  # 1 heure
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Instance globale des paramètres
settings = Settings()

# Créer les dossiers nécessaires
def create_directories():
    """Créer les dossiers nécessaires s'ils n'existent pas"""
    directories = [
        settings.static_dir,
        settings.locales_dir,
        settings.data_dir,
        settings.static_dir / "css",
        settings.static_dir / "js",
        settings.static_dir / "images",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        
    print("✅ Dossiers créés avec succès")

if __name__ == "__main__":
    create_directories()