#### schemas/suplement.py

from pydantic import BaseModel
from pydantic.config import ConfigDict

# Osnovna šema – zajednički atributi
class SuplementBase(BaseModel):
    naziv: str

# Za unos novog suplementa
class SuplementCreate(SuplementBase):
    pass

# Za slanje suplementa u odgovoru (npr. GET /api/suplementi)
class SuplementOut(SuplementBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

# Ovo je nedostajalo – koristi se za čitanje podataka
class SuplementRead(SuplementBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

