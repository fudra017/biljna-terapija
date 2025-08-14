#### schemas/preporuka.py

from pydantic import BaseModel
from typing import Optional, List
from pydantic.config import ConfigDict
from datetime import datetime

class PreporukaBase(BaseModel):
    dijagnoza: str
    metoda: str
    terapija_opis: Optional[str] = None
    referenca: Optional[str] = None
    biljke: List[int] = []
    suplementi: List[int] = []

class PreporukaCreate(PreporukaBase):
    pass

class PreporukaOut(PreporukaBase):
    id: int

class PreporukaRead(PreporukaBase):
    id: int
    kreirano: datetime

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2 način

