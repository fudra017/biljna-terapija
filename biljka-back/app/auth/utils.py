# app/auth/utils.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.config import settings

# Konfiguracija za bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


