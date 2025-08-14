# app/api/analiza.py

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import get_db
from app.models.korisnik import Korisnik
from app.models.analiza import Analiza as AnalizaModel
from app.models.parametri import ParametriAnalize
from app.schemas.analiza import AnalizaCreate, AnalizaOut, AnalizaRead   # Pydantic šema
from app.api.auth_routes import get_current_user
from app.utils.email import posalji_email

# nakon uspešnog čuvanja analize...
preporuka = "Ovo je vaša biljna terapija. Uskoro će sadržaj biti personalizovan."

import json

#Priprema za dodatne funkcije – koristi ako treba:
#from app.utils.pdf import generate_pdf_from_analiza       
#from app.models.istorijat import Istorijat

router = APIRouter()

# GET /api/analiza – vraća sve analize
@router.get("/", response_model=list[AnalizaRead])
def get_all_analize(db: Session = Depends(get_db)):
    return db.query(AnalizaModel).all()

@router.post("/create", response_model=AnalizaOut, status_code=status.HTTP_201_CREATED)
async def kreiraj_analizu(
    request: Request,
    analiza: AnalizaCreate,
    db: Session = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user)
):
    raw_body = await request.json()
    print("🟡 RAW body sa frontenda:\n", raw_body)

    try:
        print("Primljeni podaci:\n", json.dumps(analiza.model_dump(), indent=2, ensure_ascii=False))

        nova_analiza = AnalizaModel(
            korisnik_id=current_user.id,
            pol=analiza.pol,
            godine=analiza.godine,
            trudnoca=analiza.trudnoca,
            komorbiditeti=analiza.komorbiditeti,
            dijagnoza=analiza.dijagnoza,
            alergije=analiza.alergije,
            fizioloski_status=analiza.fizioloski_status.model_dump() if analiza.fizioloski_status else None,
            nutritivni_status = analiza.nutritivni_status.model_dump() if analiza.nutritivni_status else None,
	    psiholoski_faktori = analiza.psiholoski_faktori.model_dump() if analiza.psiholoski_faktori else None,
            zivotni_stil=analiza.zivotni_stil.model_dump() if analiza.zivotni_stil else None,
            genetski_faktori=analiza.genetski_faktori.model_dump() if analiza.genetski_faktori else None,
            okruzenje=analiza.okruzenje.model_dump() if analiza.okruzenje else None,
        )

        db.add(nova_analiza)
        db.commit()
        db.refresh(nova_analiza)
        # 📩 Poziv za slanje emaila sa preporukom
        preporuka = "Ovo je vaša biljna terapija. Uskoro će sadržaj biti personalizovan."
        posalji_email(preporuka, current_user.email)

        return nova_analiza

    except SQLAlchemyError as err:
        db.rollback()
        print("❌ Greška:", err)
        
        raise HTTPException(status_code=500, detail="Greška prilikom čuvanja analize.")

# ✅ Ruta: korisnik vidi SAMO SVOJE analize
@router.get("/moje", response_model=list[AnalizaOut])
def dohvati_moje_analize(
    db: Session = Depends(get_db),
    korisnik: Korisnik = Depends(get_current_user)
):
    return db.query(AnalizaModel).filter(AnalizaModel.korisnik_id == korisnik.id).all()


# ⚠️ Ruta: ADMIN vidi SVE analize (za test, može se ograničiti kasnije)
@router.get("/sve", response_model=list[AnalizaOut])
def dohvati_sve_analize(
    db: Session = Depends(get_db),
    korisnik: Korisnik = Depends(get_current_user)
):
    return db.query(AnalizaModel).all()


@router.put("/{analiza_id}", response_model=AnalizaOut, status_code=200)
def izmeni_analizu(
    analiza_id: int,
    izmena: AnalizaCreate,
    db: Session = Depends(get_db),
    korisnik: Korisnik = Depends(get_current_user)
):
    analiza = db.query(AnalizaModel).filter_by(id=analiza_id, korisnik_id=korisnik.id).first()
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
    analiza.zivotni_stil	       = flat_status(izmena.zivotni_stil)
    analiza.genetski_faktori   = flat_status(izmena.genetski_faktori)
    analiza.okruzenje          = flat_status(izmena.okruzenje)

    db.commit()
    db.refresh(analiza)

    return analiza

@router.get("/moje", response_model=list[AnalizaRead])
async def get_analize_korisnika(
    db: Session = Depends(get_db),
    korisnik: Korisnik = Depends(get_current_user)
):
    analize = db.query(AnalizaModel).filter(AnalizaModel.korisnik_id == korisnik.id).all()
    return analize
