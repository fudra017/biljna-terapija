#app\api\preporuka.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.preporuka import Preporuka  # SQLAlchemy model
from app.schemas.preporuka import PreporukaCreate, PreporukaRead  # Pydantic šeme

router = APIRouter()

@router.get("/preporuke", response_model=list[PreporukaRead])  # Moja ranija funkcija
def get_preporuke(db: Session = Depends(get_db)):
    return db.query(Preporuka).all()

@router.post("/preporuke/create", tags=["Preporuke"])
def kreiraj_preporuku():
    return {"msg": "Preporuka kreirana"}
