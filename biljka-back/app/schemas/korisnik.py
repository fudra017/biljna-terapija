# === app/schemas/korisnik.py ===
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Literal

# ----------------------------
# Osnovni model korisnika
# ----------------------------
class KorisnikBase(BaseModel):
    ime: str
    prezime: str
    email: EmailStr
    uloga: Literal["korisnik", "lekar", "admin"] = "korisnik"  # ⬅️ dodato

# ----------------------------
# Model za kreiranje korisnika
# ----------------------------
class KorisnikCreate(KorisnikBase):
    sifra: str

    @field_validator("sifra")
    @classmethod
    def validacija_sifre(cls, vrednost):
        if len(vrednost) < 6:
            raise ValueError("Šifra mora imati bar 6 karaktera.")
        return vrednost

# ----------------------------
# Model za javni prikaz
# ----------------------------
class KorisnikPublic(BaseModel):
    id: int
    ime: str
    prezime: str
    email: EmailStr
    uloga: Literal["korisnik", "lekar", "admin"] = "korisnik"  # ⬅️ dodato

    class Config:
        from_attributes = True

# ----------------------------
# Model za prikaz korisnika sa dodatnim info
# ----------------------------
class KorisnikOut(KorisnikPublic):
    admin: bool
    datum_registracije: datetime

    class Config:
        from_attributes = True
