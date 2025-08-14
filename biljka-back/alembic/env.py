import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ➊ Učitaj .env varijable
load_dotenv()

# ➋ Alembic config
config = context.config
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ➌ Logging (ako je podešen u alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ➍ Dodaj projektni root u sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ➎ Uvezi Base i sve modele
from app.database.base import Base
from app.models import korisnik, parametri, preporuka, istorijat, biljka, suplement, analiza  # ⬅️ modeli

target_metadata = Base.metadata

# OFFLINE MIGRACIJA
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ONLINE MIGRACIJA
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# START
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
