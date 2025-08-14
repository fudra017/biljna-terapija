# init_db.py
# pokrećeš ga samo kada treba da inicijalizuješ šemu:
# sledećom komandom:
# python -m app.database.init_db


from app.database import engine, Base
from app.models import pacijent, terapija  # Dodaj sve modele

Base.metadata.create_all(bind=engine)
