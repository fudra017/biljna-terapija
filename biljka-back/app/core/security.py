# app/core/security.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.settings import settings
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- GET PASSWORD ----------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---------- VERIFY PASSWORD ----------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ----------CREATE ACCESS TOKEN ----------
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    print("🛡️ SECRET_KEY za kreiranje:", settings.SECRET_KEY) # Dodato za atest
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# ---------- VERIFY TOKEN ----------
def verify_token(token: str) -> dict:
    print("🔐 SECRET_KEY za verifikaciju:", settings.SECRET_KEY)   # Dodato radi testa
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neispravan token",
            headers={"WWW-Authenticate": "Bearer"},
        )



