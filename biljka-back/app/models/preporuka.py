#### models/preporuka.py

from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

# Many-to-many povezivanje preporuka i biljaka
preporuka_biljke = Table(
    'preporuka_biljke', Base.metadata,
    Column('preporuka_id', ForeignKey('preporuke.id', ondelete="CASCADE"), primary_key=True),
    Column('biljka_id', ForeignKey('biljke.id', ondelete="CASCADE"), primary_key=True)
)

# Many-to-many povezivanje preporuka i suplemenata
preporuka_suplementi = Table(
    'preporuka_suplementi', Base.metadata,
    Column('preporuka_id', ForeignKey('preporuke.id', ondelete="CASCADE"), primary_key=True),
    Column('suplemenat_id', ForeignKey('suplementi.id', ondelete="CASCADE"), primary_key=True)
)

class Preporuka(Base):
    __tablename__ = 'preporuke'

    id = Column(Integer, primary_key=True, index=True)
    dijagnoza = Column(String, nullable=False)
    metoda = Column(String, nullable=False)
    terapija_opis = Column(Text, nullable=True)
    referenca = Column(Text, nullable=True)

    biljke = relationship("Biljka", secondary=preporuka_biljke)
    suplementi = relationship("Suplement", secondary=preporuka_suplementi)

    istorijat = relationship("Istorijat", back_populates="preporuka")


