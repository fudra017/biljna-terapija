#### schemas/istorijat.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .korisnik import KorisnikOut
#from .parametri import ParametriOut
from .analiza import AnalizaOut   # Zamena za gornji red
from .preporuka import PreporukaOut
from pydantic.config import ConfigDict

class IstorijatBase(BaseModel):
    korisnik_id: int
    parametri_id: int
    preporuka_id: Optional[int] = None
    tip_usluge: str
    rezultat_pdf: Optional[str] = ""

class IstorijatCreate(BaseModel):
    korisnik_id: int
    parametri_id: int
    preporuka_id: int
    tip_usluge: str
    rezultat_pdf: Optional[str] = None

class IstorijatOut(BaseModel):
    id: int
    datum: datetime
    tip_usluge: str
    rezultat_pdf: Optional[str]
    korisnik: KorisnikOut
#   parametri: ParametriOut
    parametri: AnalizaOut  # Zamena za gornju liniju.
    preporuka: PreporukaOut

    class Config:
        model_config = ConfigDict(from_attributes=True)