# app/schemas/token.py
from pydantic import BaseModel
from app.schemas.korisnik import KorisnikPublic
from pydantic.config import ConfigDict

class TokenSaKorisnikom(BaseModel):
    access_token: str
    token_type: str
    user: KorisnikPublic

#   model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True  # ✅ ovo Pydantic 2 prepoznaje kao validno