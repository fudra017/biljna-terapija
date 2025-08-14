# models/__ini__.py

from .korisnik import Korisnik
from .parametri import ParametriAnalize
from .preporuka import Preporuka, preporuka_biljke, preporuka_suplementi
from .istorijat import Istorijat
from .biljka import Biljka
from .suplement import Suplement
from .analiza import Analiza

__all__ = [
    "Korisnik",
    "ParametriAnalize",
    "Preporuka",
    "preporuka_biljke",
    "preporoka_suplemeti",
    "Istorijat",
    "Biljka",
    "Suplement",
    "Analiza",
]

