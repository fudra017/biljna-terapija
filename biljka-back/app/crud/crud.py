from app.core.security import get_password_hash
from app.core.security import get_password_hash, verify_password, create_access_token
from sqlalchemy.orm import Session
from app.models.korisnik import Korisnik
from app.models.parametri import ParametriAnalize
from app.models.preporuka import Preporuka
from app.models.istorijat import Istorijat
from app.models.biljka import Biljka
from app.models.suplement import Suplement
from app.models.analiza import Analiza

from app.schemas.korisnik import KorisnikBase
#from app.schemas.parametri import ParametriBase
from app.schemas.analiza import AnalizaCreate
from app.schemas.preporuka import PreporukaBase
from app.schemas.istorijat import IstorijatCreate
from app.schemas.biljka import BiljkaBase
from app.schemas.suplement import SuplementBase
from datetime import datetime

# === Korisnici ===

def create_korisnik(db: Session, korisnik: KorisnikBase):
 ### crud/crud.py   
    hashed_password = get_password_hash(korisnik.sifra)
    print(hashed_password)
    db_korisnik = Korisnik(
        ime=korisnik.ime,
        prezime=korisnik.prezime,
        email=korisnik.email,
        #sifra=korisnik.sifra,
	sifra=hashed_password,  # OVDE MORA BITI HEŠIRANA LOZINKA
	uloga="korisnik",
	admin=False
    )
    db.add(db_korisnik)
    db.commit()
    db.refresh(db_korisnik)
    return db_korisnik


def get_korisnik_by_email(db: Session, email: str):
    return db.query(Korisnik).filter(Korisnik.email == email).first()

def get_korisnik_by_id(db: Session, korisnik_id: int):
    return db.query(Korisnik).filter(Korisnik.id == korisnik_id).first()

def get_korisnik(db: Session, korisnik_id: int):
    return db.query(Korisnik).filter(Korisnik.id == korisnik_id).first()


# === Parametri analize ===

def create_parametri(db: Session, parametri: AnalizaCreate, korisnik_id: int):
    db_parametri = ParametriAnalize(**parametri.dict(), korisnik_id=korisnik_id)
    db.add(db_parametri)
    db.commit()
    db.refresh(db_parametri)
    return db_parametri

# === Biljke i suplementi ===

def get_biljke_by_ids(db: Session, biljke_ids: list[int]):
    return db.query(Biljka).filter(Biljka.id.in_(biljke_ids)).all()

def get_suplemente_by_ids(db: Session, suplementi_ids: list[int]):
    return db.query(Suplement).filter(Suplement.id.in_(suplementi_ids)).all()


# === Preporuka ===

def create_preporuka(db: Session, preporuka: PreporukaBase):
    biljke = get_biljke_by_ids(db, preporuka.biljke)
    suplementi = get_suplemente_by_ids(db, preporuka.suplementi)
    db_preporuka = Preporuka(
        metoda=preporuka.metoda,
        terapija_opis=preporuka.terapija_opis,
        referenca=preporuka.referenca,
        biljke=biljke,
        suplementi=suplementi
    )
    db.add(db_preporuka)
    db.commit()
    db.refresh(db_preporuka)
    return db_preporuka


# === Istorijat ===

def create_istorijat(db: Session, istorijat: IstorijatCreate):
    db_istorija = Istorijat(
        korisnik_id=istorijat.korisnik_id,
        parametri_id=istorijat.parametri_id,
        preporuka_id=istorijat.preporuka_id,
        tip_usluge=istorijat.tip_usluge,
        rezultat_pdf=istorijat.rezultat_pdf,
        datum=datetime.utcnow()
    )
    db.add(db_istorija)
    db.commit()
    db.refresh(db_istorija)
    return db_istorija


def get_istorijat_po_korisniku(db: Session, korisnik_id: int):
    return db.query(Istorijat).filter(Istorijat.korisnik_id == korisnik_id).all()
