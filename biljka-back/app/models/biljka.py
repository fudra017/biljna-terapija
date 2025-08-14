#### models/biljka.py

from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Biljka(Base):
    __tablename__ = 'biljke'

    id = Column(Integer, primary_key=True, index=True)
    naziv = Column(String, unique=True)
