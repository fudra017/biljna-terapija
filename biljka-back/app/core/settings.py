
# app/core/settings.py

#  (Pydantic v2)

#    class Config:   od starog fajla
#        env_file = ".env" od starog fajla.

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 🔐 JWT konfiguracija
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 🛢️ Baza
    DATABASE_URL: str
    DEBUG: bool = False

    # 📧 Settings za Email variable
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_PORT: int = 587
    EMAIL_HOST: str = "smtp.gmail.com"

    # ⚙️ Pydantic v2 način za .env konfiguraciju
    model_config = SettingsConfigDict(env_file=".env")

# Instanca za korišćenje
settings = Settings()
