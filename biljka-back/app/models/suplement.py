#### models/suplement.py

from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Suplement(Base):
    __tablename__ = 'suplementi'

    id = Column(Integer, primary_key=True, index=True)
    naziv = Column(String, unique=True)