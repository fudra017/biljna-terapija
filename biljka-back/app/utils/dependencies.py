# utils/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
from models import Korisnik
from utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Neispravna autentifikacija.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        korisnik_id: int = payload.get("sub")
        if korisnik_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    korisnik = db.query(Korisnik).filter(Korisnik.id == korisnik_id).first()
    if korisnik is None:
        raise credentials_exception
    return korisnik


