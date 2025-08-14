# app/__init__.py

from dotenv import load_dotenv
import os

# Učitaj .env fajl odmah pri inicijalizaciji modula app
load_dotenv()

# Ovde možeš centralno definisati važne konfiguracije
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
