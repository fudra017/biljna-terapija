# schemas/analiza.py

from pydantic import Field, model_validator
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Literal, Dict

# -----------------------------
# 1. Podmodeli za svaki status
# -----------------------------

Ocena = Literal["Dobar", "Srednji", "Loš"]

class FizioloskiStatus(BaseModel):
    vitalne_funkcije: Optional[Ocena] = None
    hronicna_stanja: Optional[Ocena] = None
    laboratorije: Optional[Ocena] = None

class NutritivniStatus(BaseModel):
    unos_makronutrijenata: Optional[Ocena] = None
    unos_mikronutrijenata: Optional[Ocena] = None
    digestivno_zdravlje: Optional[Ocena] = None

class PsiholoskiFaktori(BaseModel):
    stres_i_anksioznost: Optional[Ocena] = None
    emocionalna_stabilnost: Optional[Ocena] = None
    kognitivna_funkcija: Optional[Ocena] = None

class Zivotni_Stil(BaseModel):
    fizicka_aktivnost: Optional[Ocena] = None
    navike_spavanja: Optional[Ocena] = None
    zavisnosti_i_poroci: Optional[Ocena] = None

class GenetskiFaktori(BaseModel):
    porodicna_anamneza: Optional[Ocena] = None
    genetska_predispozicija: Optional[Ocena] = None
    hronicne_bolesti_u_porodici: Optional[Ocena] = None

class Okruzenje(BaseModel):
    zagadjenje_i_toksini: Optional[Ocena] = None
    uslovi_stanovanja: Optional[Ocena] = None
    socioekonomski_faktori: Optional[Ocena] = None

# --------------------------------------
# 2. Glavni modeli za kreiranje i izlaz
# --------------------------------------

from app.schemas.parametri import (
    FizioloskiStatus,
    NutritivniStatus,
    PsiholoskiFaktori,
    ZivotniStil,
    GenetskiFaktori,
    Okruzenje
)

# === BAZNA KLASA SA VALIDACIJOM ===
class AnalizaBase(BaseModel):
    godine: Optional[int] = Field(default=None)
    pol: Optional[Literal["Muški", "Ženski"]] = Field(default=None)
    dijagnoza: Optional[str] = Field(default=None)
    komorbiditeti: Optional[str] = Field(default=None)
    alergije: Optional[str] = Field(default=None)
    trudnoca: Optional[bool] = Field(default=None)

    fizioloski_status: Optional[FizioloskiStatus] = Field(default=None)
    nutritivni_status: Optional[NutritivniStatus] = Field(default=None)
    psiholoski_faktori: Optional[PsiholoskiFaktori] = Field(default=None)
    zivotni_stil: Optional[ZivotniStil] = Field(default=None)
    genetski_faktori: Optional[GenetskiFaktori] = Field(default=None)
    okruzenje: Optional[Okruzenje] = Field(default=None)

    @model_validator(mode="after")
    def validiraj_trudnocu(self):
        if self.pol == "Muški" and self.trudnoca:
            raise ValueError("Muškarac ne može biti trudan.")
        return self

# === CREATE: koristi sve iz AnalizaBase  Znači da radi potpuno isto kao AnalizaBase ===
class AnalizaCreate(BaseModel):
    godine: Optional[int] = Field(default=None)
    pol: Optional[Literal["Muški", "Ženski"]] = Field(default=None)
    dijagnoza: Optional[str] = Field(default=None)
    komorbiditeti: Optional[str] = Field(default=None)
    alergije: Optional[str] = Field(default=None)
    trudnoca: Optional[bool] = Field(default=None)

    fizioloski_status: Optional[FizioloskiStatus] = Field(default=None)
    nutritivni_status: Optional[NutritivniStatus] = Field(default=None)
    psiholoski_faktori: Optional[PsiholoskiFaktori] = Field(default=None)
    zivotni_stil: Optional[ZivotniStil] = Field(default=None)
    genetski_faktori: Optional[GenetskiFaktori] = Field(default=None)
    okruzenje: Optional[Okruzenje] = Field(default=None)

    @model_validator(mode="after")
    def validiraj_trudnocu(self):
        if self.pol == "Muški" and self.trudnoca:
            raise ValueError("Muškarac ne može biti trudan.")
        return self



class AnalizaOut(BaseModel):
    id: int
    korisnik_id: int
    godine: Optional[int] = None
    pol: Optional[Literal["Muški", "Ženski"]] = None
    dijagnoza: Optional[str] = None
    komorbiditeti: Optional[str] = None
    alergije: Optional[str] = None
    trudnoca: Optional[bool] = None

    fizioloski_status: Optional[FizioloskiStatus] = None
    nutritivni_status: Optional[NutritivniStatus] = None
    psiholoski_faktori: Optional[PsiholoskiFaktori] = None
    zivotni_stil: Optional[ZivotniStil] = None
    genetski_faktori: Optional[GenetskiFaktori] = None
    okruzenje: Optional[Okruzenje] = None

    model_config = ConfigDict(from_attributes=True)


# === READ: koristi se za čitanje sa dodatnim timestamp-om Potpuno nasleđuje AnalizaOut ===
class AnalizaRead(AnalizaOut):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    timestamp: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)