#### models/parametri.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.base import Base

class ParametriAnalize(Base):
    __tablename__ = 'parametri'

    id = Column(Integer, primary_key=True, index=True)
    korisnik_id = Column(Integer, ForeignKey("korisnici.id"))
    pol = Column(String)
    godine= Column(Integer)
    trudnoca = Column(Boolean, default=False)
    komorbiditeti = Column(Text)
    dijagnoza = Column(Text)
    alergije = Column(Text) ### alergije = Column(String, nullable=True)
    fizioloski_status = Column(Text)
    nutritivni_status = Column(Text)
    psiholoski_faktori = Column(Text)
    zivotni_stil= Column(Text)
    genetski_faktori = Column(Text)
    okruzenje = Column(Text)

    istorijat = relationship("Istorijat", back_populates="parametri")
    korisnik = relationship("Korisnik", back_populates="parametri")