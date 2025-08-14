# app/api/suplement.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.suplement import Suplement
from app.schemas.suplement import SuplementRead
from typing import List

router = APIRouter()

@router.get("/", response_model=List[SuplementRead])
def svi_suplementi(db: Session = Depends(get_db)):
    return db.query(Suplement).all()

@router.post("/suplementi/create", tags=["Suplementi"])
def dodaj_suplement():
    return {"msg": "Suplement dodat"}



