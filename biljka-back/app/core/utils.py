# utils.py
from datetime import datetime
from typing import Optional
import re

def format_datum(timestamp: Optional[datetime] = None) -> str:
    """Vraća datum u formatu dd.mm.yyyy."""
    if not timestamp:
        timestamp = datetime.now()
    return timestamp.strftime("%d.%m.%Y")

def validiraj_email(email: str) -> bool:
    """Jednostavna validacija e-mail adrese."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def skratak(tekst: str, duzina: int = 100) -> str:
    """Skrati tekst na zadatu dužinu sa tri tačke."""
    if len(tekst) <= duzina:
        return tekst
    return tekst[:duzina].rstrip() + "..."

def log_poruka(akcija: str, detalj: str = "") -> None:
    """Jednostavan log u terminal."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {akcija} -- {detalj}")
