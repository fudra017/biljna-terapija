#### schemas/parametri_prethodni.py

from pydantic import BaseModel
from typing import Optional, Literal

class FizioloskiStatus(BaseModel):
    vitalne_funkcije: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    hronicna_stanja: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    laboratorije: Optional[Literal["Dobar", "Srednji", "Loš"]] = None

class NutritivniStatus(BaseModel):
    unos_makronutrijenata: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    unos_mikronutrijenata: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    digestivno_zdravlje: Optional[Literal["Dobar", "Srednji", "Loš"]] = None

class PsiholoskiFaktori(BaseModel):
    stres_i_anksioznost: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    emocionalna_stabilnost: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    kognitivna_funkcija: Optional[Literal["Dobar", "Srednji", "Loš"]] = None

class ZivotniStil(BaseModel):
    fizicka_aktivnost: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    navike_spavanja: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    zavisnosti_i_poroci: Optional[Literal["Dobar", "Srednji", "Loš"]] = None

class GenetskiFaktori(BaseModel):
    porodicna_anamneza: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    genetska_predispozicija: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    hronicne_bolesti_u_porodici: Optional[Literal["Dobar", "Srednji", "Loš"]] = None

class Okruzenje(BaseModel):
    zagadjenje_i_toksini: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    uslovi_stanovanja: Optional[Literal["Dobar", "Srednji", "Loš"]] = None
    socioekonomski_faktori: Optional[Literal["Dobar", "Srednji", "Loš"]] = None

