# app/api/korisnik.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db # Ovo je ispravno
from app.models.korisnik import Korisnik
from app.schemas.korisnik import KorisnikCreate, KorisnikOut
from app.core.security import get_password_hash, create_access_token 
from app.core.settings import settings

router = APIRouter()

@router.get("/me", tags=["Autentikacija"])
def get_me():
    return {"ime": "Draško", "email": "primer@mail.com"}



@router.post("/registracija", status_code=201)
def registruj_korisnika(korisnik: KorisnikCreate, db: Session = Depends(get_db)):
    # 1. Proveri da li korisnik već postoji
    postojeci = db.query(Korisnik).filter(Korisnik.email == korisnik.email).first()
    if postojeci:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Korisnik sa ovom email adresom već postoji."
        )

    # 2. Hashuj lozinku
    hashed_sifra = get_password_hash(korisnik.sifra)

    # 3. Kreiraj novog korisnika
    novi_korisnik = Korisnik(
        ime=korisnik.ime,
        prezime=korisnik.prezime,
        email=korisnik.email,
        sifra=hashed_sifra
    )
    db.add(novi_korisnik)
    db.commit()
    db.refresh(novi_korisnik)

    # 4. Napravi JWT token
    token = create_access_token(data={"id": novi_korisnik.id})

    # 5. Kreiraj izlazni model korisnika (npr. bez lozinke)
    korisnik_out = KorisnikOut(
        id=novi_korisnik.id,
        ime=novi_korisnik.ime,
        prezime=novi_korisnik.prezime,
        email=novi_korisnik.email,
        admin=novi_korisnik.admin,
        datum_registracije=novi_korisnik.datum_registracije
    )

    # 6. Vrati rezultat
    return {
        "poruka": "Uspešno registrovan korisnik",
        "access_token": token,
        "token_type": "bearer",
        "user": korisnik_out
    }