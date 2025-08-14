# create_tables.py
from models import Base  # Uvozimo iz models, jer tamo se nalazi Base
from database import engine

Base.metadata.create_all(bind=engine)