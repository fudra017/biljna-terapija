# Biljna terapija
ECHO is on.
Monorepo:
- /biljka-front - Vite/React frontend
- /biljka-back  - FastAPI backend

Biljna terapija — monorepo

Full-stack aplikacija za preporuku biljnih i suplementnih terapija.
Monorepo sadrži React (Vite) frontend i FastAPI backend.

/biljka-front   # Vite/React frontend
/biljka-back    # FastAPI backend

Sadržaj

Opis

Preduslovi

Struktura repozitorijuma

Frontend — start, build, deploy

Backend — start, DB, migracije

Primer .env fajlova

Tipične zamke (obavezno pročitati)

Git & grane

Plan razvoja / next steps

Opis

Aplikacija omogućava:

izbor dijagnoze iz baze (~400+ stavki),

generisanje standardne ili personalizovane preporuke,

prikaz biljaka, suplemenata i referenci,

čuvanje istorije analiza (backend + DB),

(u planu) PDF eksport, email obaveštenja, fiskalizacija i sl.

Preduslovi

Frontend

Node.js ≥ 18 LTS (preporuka 20.x)

NPM (dolazi sa Node-om)

Backend

Python 3.10.x

PostgreSQL 16 (lokalno ili udaljeno)

Git 2.4x+

(Windows korisnici: preporuka je da radite iz CMD ili PowerShell; Git Bash je OK ali paziti na putanje.)

Struktura repozitorijuma
biljna-terapija/
 ├─ biljka-front/
 │   ├─ src/               # React kod
 │   ├─ public/            # static assets
 │   ├─ package.json
 │   └─ vite.config.js
 ├─ biljka-back/
 │   ├─ app/
 │   │   ├─ api/           # FastAPI rute
 │   │   ├─ core/          # settings, security
 │   │   ├─ database/      # konekcija, session, init
 │   │   ├─ models/        # SQLAlchemy modeli
 │   │   ├─ schemas/       # Pydantic šeme
 │   │   └─ utils/         # pomoćne funkcije
 │   ├─ alembic/           # migracije
 │   ├─ alembic.ini
 │   ├─ requirements.txt
 │   └─ app/main.py        # FastAPI app ulaz
 ├─ .gitignore
 └─ README.md

Frontend — start, build, deploy
1) Instalacija
cd biljka-front
npm install

2) Lokalni razvoj (Vite dev server)
npm run dev


Podrazumevano na: http://localhost:5173

Ako API radi na http://127.0.0.1:8000, proveri CORS u backendu (vidi dole).

3) Build (produkcija)
npm run build


Artefakti u biljka-front/dist/.

4) Deploy (Netlify primer)

Kreiraj sajt na Netlify, poveži na GitHub repo/granu.

Build command: npm run build

Publish dir: biljka-front/dist

Ako koristiš SPA rute, u public/_redirects.txt drži:

/* /index.html 200

Backend — start, DB, migracije
1) Kreiraj i aktiviraj venv
cd biljka-back
python -m venv venv
venv\Scripts\activate

2) Instalacija zavisnosti
pip install --upgrade pip
pip install -r requirements.txt

3) Podesi okruženje (.env)

Kreiraj biljka-back/.env (primer niže u dokumentu). Najbitnije:

DATABASE_URL (PostgreSQL konekcija)

SECRET_KEY (JWT)

ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

(opciono) email SMTP parametri, CORS liste, itd.

4) Inicijalizuj bazu / migracije (Alembic)

Prvi put (ako baza prazna):

alembic upgrade head


Kada menjaš modele:

alembic revision -m "opis promene"
alembic upgrade head


Alembic čita alembic.ini i alembic/env.py. Uveri se da target_metadata pokazuje na tvoje SQLAlchemy modele.

5) Pokreni backend server
uvicorn app.main:app --reload


Podrazumevano na: http://127.0.0.1:8000

Zdravo-test: otvori http://127.0.0.1:8000/docs (Swagger UI).

6) CORS (bitno)

U app/main.py ili app/core/settings.py proširi allow_origins da uključiš frontend:

za lokalni dev: http://localhost:5173

za Netlify deploy: https://<tvoj-netlify-sajt>.netlify.app

Primer .env fajlova

Nikada ne komitovati prave tajne (.env je u .gitignore). Ako su bilo kakvi ključevi/tokene već završili u repo-u, obavezno rotiraj (promeni) te ključeve i obriši fajlove iz istorije po potrebi.

biljka-back/.env (primer)
# App
APP_NAME=BiljnaTerapija
ENV=dev
DEBUG=True

# Security / JWT
SECRET_KEY=promeni_me_na_slučajnu_dugačku_vrednost
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# Database (PostgreSQL)
# Primer lokalno:
DATABASE_URL=postgresql+psycopg2://postgres:lozinka@localhost:5432/biljka_baza
# Primer udaljeno (Render, Railway, itd.):
# DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname

# CORS
ALLOWED_ORIGINS=http://localhost:5173,https://<tvoj-netlify>.netlify.app

# Email (opciono)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tvoj_nalog@gmail.com
SMTP_PASS=app_password_ili_token
EMAIL_FROM=tvoj_nalog@gmail.com

biljka-front/.env (primer)

Ako koristiš Vite, prefiks promenljivih je VITE_.

VITE_API_BASE_URL=http://127.0.0.1:8000
# npr: VITE_API_BASE_URL=https://api.tvoj-domen.rs


U kodu (React):

const baseURL = import.meta.env.VITE_API_BASE_URL;

Tipične zamke (obavezno pročitati)

Ne komituj tajne: .env, API ključeve, lozinke.
Ako si slučajno dodao fajlove tipa:

Token za autorizaciju.txt

Secret_key ... .txt

Lozinka ... .txt

→ Obriši ih iz repoa i rotiraj (promeni) te podatke.
Brisanje sadašnjih fajlova:

git rm --cached "biljka-back/Token za autorizaciju.txt"
git rm --cached "biljka-back/Token za autorizaciju i Secret_kay za aplikaciju i Lozinka za PostgreSQL16.txt"
git rm --cached "biljka-back/O secret kay u i tokenu Secret_kay za aplikaciju i Lozinka za PostgreSQL16.txt"
git commit -m "remove: sensitive plaintext files"
git push


Ako želiš i iz istorije da ih skineš (rewrite history), javi — daću ti bezbedne komande (npr. git filter-repo) + savet za rotaciju svih ključeva.

CRLF/LF upozorenja na Windowsu su normalna.
Ako hoćeš da utišaš:

git config core.autocrlf true


Embedded repo (submodule): Ako se opet pojavi poruka “adding embedded git repository”, znači da je u podfolderu ostao skriven .git. Obrisi ga:

rmdir /S /Q "putanja\do\podfoldera\.git"
git rm --cached -r putanja\do\podfoldera
git add putanja\do\podfoldera


node_modules / dist / venv: nikad ne guraj u repo (već su u .gitignore).

Git & grane

Glavna grana: master

Legacy snapshot sa starim kodom:

grana: legacy/pre-restructure-2025-08-15

tag: v0-legacy-2025-08-15

Preporučeni tok rada

git checkout -b feat/naziv-funkcionalnosti
... radiš izmene ...
git add -A
git commit -m "feat: opis"
git push -u origin HEAD
# (opciono) PR preko GitHub-a ka master

Plan razvoja / next steps

 Proširi README sa slikama ekrana (front) i primerima API poziva (back).

 Dodaj /docs folder za arhitekturu (sekvence, modeli).

 Uvedi .env.example fajlove u oba modula.

 Postavi CORS origin(e) za produkciju (Netlify domen).

 (Opciono) GitHub Actions:

Frontend: build & deploy na Netlify/Vercel.

Backend: test + deploy (Render/Railway/VPS).

 Ukloni iz repoa sve tekstualne fajlove sa lozinkama/secretima i rotiraj vrednosti.
