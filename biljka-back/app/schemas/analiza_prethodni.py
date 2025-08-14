# schemas/analiza.py

from pydantic import Field, model_validator
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# -----------------------------
# 1. Podmodeli za svaki status
# -----------------------------

Ocena = Literal["Dobar", "Srednji", "Loš"]

class FizioloskiStatus(BaseModel):
    vitalne_funkcije: Ocena = "Dobar"
    hronicna_stanja: Ocena = "Dobar"
    laboratorije: Ocena = "Dobar"

class NutritivniStatus(BaseModel):
    unos_makronutrijenata: Ocena = "Dobar"
    unos_mikronutrijenata: Ocena = "Dobar"
    digestivno_zdravlje: Ocena = "Dobar"

class PsiholoskiFaktori(BaseModel):
    stres_i_anksioznost: Ocena = "Dobar"
    emocionalna_stabilnost: Ocena = "Dobar"
    kognitivna_funkcija: Ocena = "Dobar"

class ZivotniStil(BaseModel):
    fizicka_aktivnost: Ocena = "Dobar"
    navike_spavanja: Ocena = "Dobar"
    zavisnosti_i_poroci: Ocena = "Dobar"

class GenetskiFaktori(BaseModel):
    porodicna_anamneza: Ocena = "Dobar"
    genetska_predispozicija: Ocena = "Dobar"
    hronicne_bolesti_u_porodici: Ocena = "Dobar"

class Okruzenje(BaseModel):
    zagadjenje_i_toksini: Ocena = "Dobar"
    uslovi_stanovanja: Ocena = "Dobar"
    socioekonomski_faktori: Ocena = "Dobar"

# --------------------------------------
# 2. Glavni modeli za kreiranje i izlaz
# --------------------------------------

# === BAZNA KLASA SA VALIDACIJOM ===
class AnalizaBase(BaseModel):
    godine: int
    pol: Literal["Muški", "Ženski"]
    dijagnoza: str
    komorbiditeti: str
    alergije: str
    trudnoca: bool
    fizioloski_status: FizioloskiStatus
    nutritivni_status: NutritivniStatus
    psiholoski_faktori: PsiholoskiFaktori
    zivotni_stil: ZivotniStil
    genetski_faktori: GenetskiFaktori
    okruzenje: Okruzenje

    @model_validator(mode="after")
    def validiraj_trudnocu(self):
        if self.pol == "Muški" and self.trudnoca:
            raise ValueError("Muškarac ne može biti trudan.")
        return self

class AnalizaCreate(BaseModel):
    godine: int
    pol: Literal["Muški", "Ženski"]
    dijagnoza: str
    komorbiditeti: str
    alergije: str
    trudnoca: bool
    fizioloski_status: FizioloskiStatus
    nutritivni_status: NutritivniStatus
    psiholoski_faktori: PsiholoskiFaktori
    zivotni_stil: ZivotniStil
    genetski_faktori: GenetskiFaktori
    okruzenje: Okruzenje

    #model_config = {
    #    "validate_by_name": True
    #}


class AnalizaOut(BaseModel):
    id: int
    korisnik_id: int
    pol: Literal["Muški", "Ženski"]
    godine: int
    trudnoca: bool
    komorbiditeti: str
    dijagnoza: str
    alergije: str
    fizioloski_status: FizioloskiStatus
    nutritivni_status: NutritivniStatus
    psiholoski_faktori: PsiholoskiFaktori
    zivotni_stil: ZivotniStil
    genetski_faktori: GenetskiFaktori
    okruzenje: Okruzenje

class AnalizaRead(BaseModel):
    id: int
    korisnik_id: int
    pol: str
    godine: int
    trudnoca: Optional[bool] = None
    dijagnoza: str
    komorbiditeti: Optional[str] = None
    alergije: Optional[str] = None

    fizioloski_status: FizioloskiStatus
    nutritivni_status: NutritivniStatus
    psiholoski_faktori: PsiholoskiFaktori
    zivotni_stil: ZivotniStil
    genetski_faktori: GenetskiFaktori
    okruzenje: Okruzenje

    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
    
model_config = ConfigDict(from_attributes=True)
