# models/analiza.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from app.database.base import Base 
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime
from datetime import datetime

timestamp = Column(DateTime, default=datetime.utcnow)

class Analiza(Base):
    __tablename__ = 'analize'

    id = Column(Integer, primary_key=True, index=True)
    godine = Column(Integer, nullable=True)
    dijagnoza = Column(String, nullable=True)
    komorbiditeti = Column(String, nullable=True)
    alergije = Column(String, nullable=True)
    pol = Column(String, nullable=False)
    trudnoca = Column(Boolean, nullable=False)  # ✅ ispravka tipa

    fizioloski_status = Column(JSON, nullable=True)
    nutritivni_status = Column(JSON, nullable=True)
    psiholoski_faktori = Column(JSON, nullable=True)
    zivotni_stil = Column(JSON, nullable=True)
    genetski_faktori = Column(JSON, nullable=True)
    okruzenje = Column(JSON, nullable=True)

    korisnik_id = Column(Integer, ForeignKey("korisnici.id"), nullable=False)
    korisnik = relationship("Korisnik", back_populates="analize")
