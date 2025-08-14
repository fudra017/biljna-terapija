# app/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings

from app.database.base import Base

# Kreiraj SQLAlchemy engine koristeći vrednost iz .env fajla
engine = create_engine(settings.DATABASE_URL)

# Sesija za rad sa bazom
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bazna klasa za ORM modele
Base = declarative_base()

# Dependency za FastAPI (ubacuje se u Depends(get_db))
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
