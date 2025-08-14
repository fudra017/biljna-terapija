# app/api/__init__.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Dobrodošli u Biljna Terapija backend API!"}
