# app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Učitavanje .env fajla
load_dotenv()

# Preuzimanje URL-a baze iz .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/biljna_terapija")

# SQLAlchemy engine i sesija
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Osnovna klasa za modele
Base = declarative_base()
