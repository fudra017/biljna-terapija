# app/database/database.py
from sqlalchemy import create_engine
from app import DATABASE_URL  		# povlači se iz __init__.py
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from dotenv import load_dotenv
import os

from .base import Base

# Učitaj .env fajl (ako ga koristiš)
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:ledra210358@localhost:5432/biljka_baza"
)

#engine = create_engine(SQLALCHEMY_DATABASE_URL)
#engine = create_engine(DATABASE_URL)
engine = create_engine(settings.DATABASE_URL)

# Lokalne sesije za pristup bazi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Osnovna klasa za modele
Base = declarative_base()

# Dependency za FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
