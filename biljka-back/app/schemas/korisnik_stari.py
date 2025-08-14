# app/schemas/korisnik.py

from pydantic import BaseModel, EmailStr, field_validator
from pydantic.config import ConfigDict
from datetime import datetime

# ✅ Osnovna baza za korisnike
class KorisnikBase(BaseModel):
    ime: str
    prezime: str
    email: EmailStr

# ✅ Model za unos prilikom registracije (sa lozinkom)
class KorisnikCreate(KorisnikBase):
    sifra: str

    @field_validator("sifra")
    @classmethod
    def validacija_sifre(cls, vrednost):
        if len(vrednost) < 6:
            raise ValueError("Šifra mora imati bar 6 karaktera.")
        return vrednost

# ✅ Model za javni prikaz korisnika – koristi se na frontend-u
#class KorisnikPublic(BaseModel):
#    id: int
#    ime: str
#    prezime: str
#    email: EmailStr

#    model_config = ConfigDict(from_attributes=True)

class KorisnikPublic(BaseModel):
    id: int
    ime: str
    prezime: str
    email: EmailStr

    class Config:
        from_attributes = True

# ✅ Model za backend izlaz (može se koristiti npr. kod /me ruta)
#class KorisnikOut(KorisnikBase):
class KorisnikOut(BaseModel):
    id: int
    ime: str
    prezime: str
    email: EmailStr
    admin: bool
    datum_registracije: datetime

    model_config = ConfigDict(from_attributes=True)  # ako koristiš Pydantic v2