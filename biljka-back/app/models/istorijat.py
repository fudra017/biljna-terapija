#### models/istorijat.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Istorijat(Base):
    __tablename__ = 'istorijat'

    id = Column(Integer, primary_key=True, index=True)
    korisnik_id = Column(Integer, ForeignKey("korisnici.id"))
    parametri_id = Column(Integer, ForeignKey("parametri.id"))
    preporuka_id = Column(Integer, ForeignKey("preporuke.id"))
    datum = Column(DateTime, default=datetime.utcnow)
    tip_usluge = Column(String)
    rezultat_pdf = Column(String)

    korisnik = relationship("Korisnik", back_populates="istorijat")
    parametri = relationship("ParametriAnalize", back_populates="istorijat")
    preporuka = relationship("Preporuka", back_populates="istorijat")
