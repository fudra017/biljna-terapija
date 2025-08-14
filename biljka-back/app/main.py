# ============================================================
# app/main.py  –  “jedna istina” o FastAPI aplikaciji
# ============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# ============================================================
# FastAPI instance  (uvek samo **jedna**!)
# ============================================================
app = FastAPI(
    title="Biljna Terapija API",
    version="1.0.0",
    description="API za upravljanje korisnicima, parametrima, preporukama i istorijatom",
)

# ⬇️ CORS middleware odmah posle inicijalizacije app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://helpful-semolina-a72bdd.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from datetime import timedelta
import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# ---------------- Database helpers ----------------
from app.database.database import get_db

# ---------------- JWT setup ----------------
from app.core.settings import settings  # koristi .env fajl
from app.core.security import create_access_token, verify_token  # koristiš funkcije iz centralnog mesta

# ---------------- ROUTERS ----------------
from app.api.korisnik import router as korisnik_router
from app.api.auth_routes import router as auth_router
from app.api.preporuka import router as preporuka_router
from app.api.suplement import router as suplement_router
from app.api import analiza

# ---------------- CURRENT USER helper ----------------
from app.api.auth_routes import get_current_user
# ---------------- CRUD sloj ----------------
from app.crud import crud  # app/crud/crud.py

# ----------------- SLANJE EMAILA KORISNICIMA ---------
from app.api import email

# ---------------- MODELS (SQLAlchemy) ----------------
from app.models.korisnik import Korisnik
from app.models.parametri import ParametriAnalize
from app.models.istorijat import Istorijat
from app.models.preporuka import Preporuka
from app.models.biljka import Biljka
from app.models.suplement import Suplement
from app.models.preporuka import preporuka_biljke, preporuka_suplementi

# ---------------- SCHEMAS (Pydantic) ----------------
from app.schemas.korisnik import KorisnikBase, KorisnikCreate, KorisnikOut
from app.schemas.istorijat import IstorijatBase, IstorijatCreate, IstorijatOut
from app.schemas.preporuka import PreporukaBase, PreporukaCreate, PreporukaOut
from app.schemas.biljka import BiljkaBase, BiljkaCreate, BiljkaOut
from app.schemas.suplement import SuplementBase, SuplementCreate, SuplementOut
from app.schemas.analiza import AnalizaBase, AnalizaCreate, AnalizaOut
#from app.schemas.token import Token
from app.schemas.token import TokenSaKorisnikom as Token
import pydantic
print("Pydantic verzija:", pydantic.__version__)

# ---------------- JWT konfiguracija ----------------
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# ============================================================
# Uključi spoljne rutere
# ============================================================

# 🔗 Registruj sve rutere

app.include_router(analiza.router,    prefix="/api/analiza", 	tags=["Analiza"])
app.include_router(auth_router,       prefix="/api/auth",       tags=["Autentikacija"])
app.include_router(korisnik_router,   prefix="/api/korisnik",   tags=["Korisnici"])
app.include_router(preporuka_router)
app.include_router(suplement_router,  prefix="/api/suplement",  tags=["Suplementi"])
app.include_router(email.router,      prefix="/api", 		tags=["Email"])


# ---------- OpenAPI Swagger JWT ----------
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Biljna Terapija API",
        version="1.0.0",
        description="Swagger dokumentacija sa JWT autentifikacijom i zaštićenim rutama",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    protected_routes = [
        "/me",
        "/analiza/create",
        "/analiza/list",
        "/istorijat",
        "/api/analiza",
    ]

    for path, methods in openapi_schema["paths"].items():
        for operation in methods.values():
            if any(path.startswith(route) for route in protected_routes):
                operation.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
