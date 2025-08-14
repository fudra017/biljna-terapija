#### schemas/parametri_prethodni.py

from pydantic import BaseModel
from typing import Literal

class FizioloskiStatus(BaseModel):
    vitalne_funkcije: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    hronicna_stanja: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    laboratorije: Literal["Dobar", "Srednji", "Loš"] = "Dobar"

class NutritivniStatus(BaseModel):
    unos_makronutrijenata: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    unos_mikronutrijenata: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    digestivno_zdravlje: Literal["Dobar", "Srednji", "Loš"] = "Dobar"

class PsiholoskiStatus(BaseModel):
    stres_i_anksioznost: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    emocionalna_stabilnost: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    kognitivna_funkcija: Literal["Dobar", "Srednji", "Loš"] = "Dobar"

class ZivotniStil(BaseModel):
    fizicka_aktivnost: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    navike_spavanja: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    zavisnosti_i_poroci: Literal["Dobar", "Srednji", "Loš"] = "Dobar"

class GenetskiStatus(BaseModel):
    porodicna_anamneza: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    genetska_predispozicija: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    hronicne_bolesti_u_porodici: Literal["Dobar", "Srednji", "Loš"] = "Dobar"

class Okruzenje(BaseModel):
    zagadjenje_i_toksini: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    uslovi_stanovanja: Literal["Dobar", "Srednji", "Loš"] = "Dobar"
    socioekonomski_faktori: Literal["Dobar", "Srednji", "Loš"] = "Dobar"

