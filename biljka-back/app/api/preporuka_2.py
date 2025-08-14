# app/api/preporuka.py
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from ..services.recommender import recommender

#router = APIRouter(prefix="/api", tags=["preporuka"])

router = APIRouter(prefix="/api/preporuka", tags=["preporuka"])

@router.get("/dijagnoze")
def get_dijagnoze():
    # Lista jedinstvenih dijagnoza (lep naziv, bez grupisanja)
    return {"dijagnoze": recommender.dijagnoze()}

@router.get("/preporuka")
def get_preporuka(bolest: str = Query(..., min_length=2)):
    data = recommender.preporuka(bolest)
    if not data:
        # Stabilna šema i kada nema pogodaka
        return {
            "bolest": bolest,
            "biljke": [],
            "suplementi": [],
            "literatura": [],
            "napomena": "Nema podataka za ovu dijagnozu."
        }
    # Stabilna šema kada ima podataka
    return {**data, "napomena": None}

# (Opcionalno) PDF endpoint – aktiviraj kada dodaš utils_pdf/rendering
@router.get("/preporuka/pdf")
def get_preporuka_pdf(bolest: str = Query(..., min_length=2)):
    data = recommender.preporuka(bolest)
    if not data or (not data["biljke"] and not data["suplementi"]):
        raise HTTPException(status_code=404, detail="Nema podataka za ovu dijagnozu.")
    # TODO: xhtml2pdf render ovde kad dodaš util
    raise HTTPException(status_code=501, detail="PDF generisanje još nije aktivirano.")









