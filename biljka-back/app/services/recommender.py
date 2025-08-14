from pathlib import Path
import pandas as pd
import re

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "sve_bolesti_objedinjeno.csv"

def _norm(text: str) -> str:
    if text is None: return ""
    return re.sub(r"\s+", " ", str(text).strip()).lower()

def _split_list(cell: str):
    if not cell: return []
    t = str(cell).strip()
    if t.lower() in {"nema biljaka", "nema suplemenata"}:
        return []
    parts = re.split(r"\s*;\s*", t)               # očekujemo ; kao separator
    return [re.sub(r"\s+", " ", p.strip()) for p in parts if p.strip()]

class Recommender:
    def __init__(self):
        self._by_diag = {}
        self._load()

    def _load(self):
        df = pd.read_csv(CSV_PATH)

        # Ignoriši 1. kolonu (Grupa bolesti) – radimo samo sa ovima:
        cols = ["Bolest", "Preporučene biljke", "Preporučeni suplementi", "Autori i naziv rada"]
        df = df[cols].copy()

        agg = {}
        for _, r in df.iterrows():
            key = _norm(r["Bolest"])
            biljke = set(_split_list(r["Preporučene biljke"]))
            supl   = set(_split_list(r["Preporučeni suplementi"]))
            lit    = set(_split_list(r["Autori i naziv rada"]))

            d = agg.setdefault(key, {
                "bolest": str(r["Bolest"]).strip(),
                "biljke": set(), "supl": set(), "lit": set()
            })
            d["biljke"].update(biljke)
            d["supl"].update(supl)
            d["lit"].update(lit)

        self._by_diag = {
            k: {
                "bolest": v["bolest"],
                "biljke": sorted(v["biljke"]),
                "suplementi": sorted(v["supl"]),
                "literatura": sorted(v["lit"]),
            } for k, v in agg.items()
        }

    def dijagnoze(self):
        return sorted({v["bolest"] for v in self._by_diag.values()})

    def preporuka(self, bolest: str):
        return self._by_diag.get(_norm(bolest))

# kreiraj singleton pri importu modula
recommender = Recommender()
