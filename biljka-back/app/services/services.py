# app/services/services.py

from sqlalchemy.orm import Session

from app.models.korisnik import Korisnik
from app.models.parametri import ParametriAnalize
from app.models.preporuka import Preporuka
from app.models.istorijat import Istorijat
from app.models.biljka import Biljka
from app.models.suplement import Suplement
from app.models.analiza import Analiza

from app.schemas.korisnik import KorisnikBase
from app.schemas.parametri import ParametriBase
from app.schemas.preporuka import PreporukaBase
from app.schemas.istorijat import IstorijatCreate
from app.schemas.biljka import BiljkaBase
from app.schemas.suplement import SuplementBase
from app.schemas.analiza import AnalizaPodataka



def kreiraj_korisnika(db: Session, korisnik: KorisnikBase):
    db_korisnik = models.Korisnik(
        ime=korisnik.ime,
        prezime=korisnik.prezime,
        email=korisnik.email,
        sifra=korisnik.sifra,
        admin=korisnik.admin if korisnik.admin is not None else False
    )
    db.add(db_korisnik)
    db.commit()
    db.refresh(db_korisnik)
    return db_korisnik


def nadji_korisnika_po_emailu(db: Session, email: str):
    return db.query(models.Korisnik).filter(models.Korisnik.email == email).first()


def sacuvaj_istorijat(db: Session, istorijat: IstorijatCreate):
    db_istorijat = models.Istorijat(**istorijat.dict())
    db.add(db_istorijat)
    db.commit()
    db.refresh(db_istorijat)
    return db_istorijat


def dohvati_preporuku(db: Session, preporuka_id: int):
    return db.query(models.Preporuka).filter(models.Preporuka.id == preporuka_id).first()


def lista_suplementa_za_preporuku(db: Session, preporuka_id: int):
    return db.query(models.Suplement).join(models.PreporukaSuplement).filter(
        models.PreporukaSuplement.preporuka_id == preporuka_id).all()


def lista_biljaka_za_preporuku(db: Session, preporuka_id: int):
    return db.query(models.Biljka).join(models.PreporukaBiljka).filter(
        models.PreporukaBiljka.preporuka_id == preporuka_id).all()
