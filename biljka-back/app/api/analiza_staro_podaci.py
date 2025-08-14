# app/api/analiza.py

from app.models.analiza import Analiza
from typing import List
#import json
#from pydantic import Field

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import get_db
from app.models.korisnik import Korisnik
from app.models.analiza import Analiza as AnalizaModel
from app.schemas.analiza import AnalizaCreate, AnalizaOut
from app.core.auth import get_current_user   # ↳ ako path drugačiji, prilagodi!

#Priprema za dodatne funkcije – koristi ako treba:
#from app.utils.pdf import generate_pdf_from_analiza       
#from app.models.istorijat import Istorijat

router = APIRouter(prefix="/api", tags=["Analiza"])

@router.post("api/analiza/create", response_model=AnalizaOut, status_code=status.HTTP_201_CREATED)
async def kreiraj_analizu(
    analiza: AnalizaCreate,
    db: Session = Depends(get_db),
    korisnik: Korisnik = Depends(get_current_user)
):
    print("✅ Usao u funkciju kreiraj_analizu")

    try:
        statusi = {
            "fizioloski_status": analiza.fizioloski_status.model_dump(),
            "nutritivni_status": analiza.nutritivni_status.model_dump(),
            "psiholoski_faktori": analiza.psiholoski_faktori.model_dump(),
            "zivotni_stil": analiza.zivotni_stil.model_dump(),
            "genetski_faktori": analiza.genetski_faktori.model_dump(),
            "okruzenje": analiza.okruzenje.model_dump(),
        }

        nova_analiza = Analiza(
    	    korisnik_id=korisnik.id,
    	    pol=podaci.pol,
    	    godine=podaci.godine,
    	    trudnoca=podaci.trudnoca,
    	    komorbiditeti=podaci.komorbiditeti,
    	    dijagnoza=podaci.dijagnoza,
    	    alergije=podaci.alergije,
    	    fizioloski_status=podaci.fizioloski_status or "Nepoznato",
    	    nutritivni_status=podaci.nutritivni_status or "Nepoznato",
    	    psiholoski_faktori=podaci.psiholoski_faktori or "Nepoznato",
    	    zivotni_stil=podaci.zivotni_stil or "Nepoznato",
    	    genetski_faktori=podaci.genetski_faktori or "Nepoznato",
    	    okruzenje=podaci.okruzenje or "Nepoznato",
    	    uloga="korisnik"
        )

        db.add(nova_analiza)
        db.commit()
        db.refresh(nova_analiza)

        return nova_analiza

    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Greška baze: {err.__class__.__name__}"
        )

@router.post("/analiza/create/pdf", response_model=AnalizaOut, status_code=status.HTTP_201_CREATED)
async def kreiraj_analizu_placena(
    podaci: AnalizaCreate,
    db: Session = Depends(get_db),
    korisnik: Korisnik = Depends(get_current_user)  # već sadrži id, email itd.
):   
    if not korisnik:
        raise HTTPException(404, "Korisnik nije pronađen")

@router.get("/list", response_model=List[AnalizaOut], status_code=200)
def lista_analiza(
    db: Session = Depends(get_db),
    korisnik: Korisnik = Depends(get_current_user)
):
    """
    ✅ Vraća sve analize koje pripadaju trenutno prijavljenom korisniku.
    📦 Rezultat je lista objekata tipa AnalizaOut.
    """
    analize = db.query(ParametriAnalize).filter_by(korisnik_id=korisnik.id).all()

    if not analize:
        raise HTTPException(status_code=404, detail="Nema sačuvanih analiza za ovog korisnika.")

    return analize

@router.put("/{analiza_id}", response_model=AnalizaOut, status_code=200) #response_model=AnalizaOut,vratiti odmah iza zareza posle "/{analiza_id}",
def izmeni_analizu(
    analiza_id: int,
    izmena: AnalizaCreate,
    db: Session = Depends(get_db),
    korisnik: Korisnik = Depends(get_current_user)
):
    """
    🟡 Ažurira analizu ako pripada trenutno prijavljenom korisniku.
    """
    analiza = db.query(ParametriAnalize).filter_by(id=analiza_id, korisnik_id=korisnik.id).first()
    if not analiza:
        raise HTTPException(404, "Analiza nije pronađena ili ne pripada korisniku")

    def flat_status(obj):
        return ", ".join(f"{k}: {v}" for k, v in obj.model_dump().items())

    analiza.pol = izmena.pol
    analiza.godine = izmena.godine
    analiza.trudnoca = izmena.trudnoca
    analiza.dijagnoza = izmena.dijagnoza
    analiza.komorbiditeti = izmena.komorbiditeti
    analiza.alergije = izmena.alergije
    analiza.fizioloski_status  = flat_status(izmena.fizioloski_status)
    analiza.nutritivni_status  = flat_status(izmena.nutritivni_status)
    analiza.psiholoski_faktori = flat_status(izmena.psiholoski_faktori)
    analiza.zivotni_stil       = flat_status(izmena.zivotni_stil)
    analiza.genetski_faktori   = flat_status(izmena.genetski_faktori)
    analiza.okruzenje          = flat_status(izmena.okruzenje)

    db.commit()
    db.refresh(analiza)

    return analiza

# DELETE endpoint za brisanje analize:
# Planirano za buduće faze — biće dozvoljeno samo lekarima i adminima.
# @router.delete("/{analiza_id}")
# def obrisi_analizu(...):
#     ...