# biljka-back/reset_baze.py

from app.database import Base, engine
from app.models import (
    Korisnik,
    ParametriAnalize,
    Preporuka,
    Istorijat,
    Biljka,
    Suplement,
    Analiza,
)

# Brisanje svih tabela (ako postoje)
print("🧨 Brišem sve postojeće tabele...")
Base.metadata.drop_all(bind=engine)

# Kreiranje novih tabela
print("✅ Kreiram nove tabele...")
Base.metadata.create_all(bind=engine)

print("🎉 Baza je resetovana i spremna.")

