# === app/api/auth_routes.py ===

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.korisnik import Korisnik
from app.schemas.korisnik import KorisnikPublic
from app.schemas.token import TokenSaKorisnikom
from app.core.security import create_access_token, verify_password, verify_token
from app.core.settings import settings
from jose import JWTError, jwt



router = APIRouter()


# OAuth2 shema za čitanje tokena iz zahteva
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
@router.post("/login", response_model=TokenSaKorisnikom)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    korisnik = db.query(Korisnik).filter(Korisnik.email == form_data.username).first()
    if not korisnik or not verify_password(form_data.password, korisnik.sifra):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pogrešan email ili lozinka"
        )

    access_token = create_access_token(data={"sub": korisnik.email, "id": korisnik.id})

    return TokenSaKorisnikom(
        access_token=access_token,
        token_type="bearer",
        user=KorisnikPublic.model_validate(korisnik)
    )

@router.get("/me", response_model=KorisnikPublic)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> KorisnikPublic:
    try:
        payload = verify_token(token)
        print("🔍 TOKEN PAYLOAD:", payload)  # 👈 Dodato za dijagnostiku
        user_id: int | None = payload.get("id")
        if user_id is None:
            print("⚠️ Token ne sadrži ID korisnika")
            raise HTTPException(status_code=401, detail="Token ne sadrži ID korisnika")
    except Exception as e:
        print(f"❌ Greška pri verifikaciji tokena: {e}")
        raise HTTPException(status_code=401, detail="Greška pri verifikaciji tokena")

    user = db.query(Korisnik).filter(Korisnik.id == user_id).first()
    if not user:
        print(f"⚠️ Korisnik sa ID {user_id} nije pronađen u bazi.")
        raise HTTPException(status_code=401, detail="Korisnik nije pronađen")

    print(f"✅ Pronađen korisnik: {user.email} (ID: {user.id})")
    return KorisnikPublic.model_validate(user)

