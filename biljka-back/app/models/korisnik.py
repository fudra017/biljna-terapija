### MODELS (SQLAlchemy modeli)

#### models/korisnik.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Korisnik(Base):
    __tablename__ = 'korisnici'

    id = Column(Integer, primary_key=True, index=True)
    ime = Column(String, nullable=False)
    prezime = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    sifra = Column(String(128), nullable=False)
    admin = Column(Boolean, default=False)
    datum_registracije = Column(DateTime, default=datetime.utcnow)

    parametri = relationship("ParametriAnalize", back_populates="korisnik")
    istorijat = relationship("Istorijat", back_populates="korisnik")
    analize = relationship("Analiza", back_populates="korisnik")