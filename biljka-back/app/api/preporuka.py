# app/api/preporuka.py
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse  # ostaje, koristićeš kada aktiviraš PDF
from ..services.recommender import recommender

# Držimo kompletan prefix ovde i NE dodajemo više /preporuka u path-ovima ispod.
router = APIRouter(prefix="/api/preporuka", tags=["preporuka"])

@router.get("/dijagnoze")
def get_dijagnoze():
    # Lista jedinstvenih dijagnoza (lep naziv, bez grupisanja)
    return {"dijagnoze": recommender.dijagnoze()}

# GLAVNI endpoint za JSON preporuku:
# /api/preporuka?bolest=Astma
@router.get("")
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

# PDF endpoint (aktiviraćeš kada dodaš xhtml2pdf render):
# /api/preporuka/pdf?bolest=Astma
@router.get("/pdf")
def get_preporuka_pdf(bolest: str = Query(..., min_length=2)):
    data = recommender.preporuka(bolest)
    if not data or (not data.get("biljke") and not data.get("suplementi")):
        raise HTTPException(status_code=404, detail="Nema podataka za ovu dijagnozu.")
    # TODO: xhtml2pdf render ovde kad dodaš util
    raise HTTPException(status_code=501, detail="PDF generisanje još nije aktivirano.")
