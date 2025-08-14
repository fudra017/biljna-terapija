"""Dodate sve tabele za početnu šemu baze podataka

Revision ID: 857f1fb9c771
Revises: None
Create Date: 2025-06-10 22:48:11.396950
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Identifikatori revizije – koristi ih Alembic za upravljanje migracijama
revision: str = '857f1fb9c771'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema – kreira sve početne tabele projekta."""
    # ------- osnovne tabele -------------------------------------------------
    op.create_table(
        "biljke",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("naziv", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("naziv"),
    )
    op.create_index(op.f("ix_biljke_id"), "biljke", ["id"], unique=False)

    op.create_table(
        "korisnici",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ime", sa.String(), nullable=True),
        sa.Column("prezime", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("sifra", sa.String(), nullable=True),
        sa.Column("admin", sa.Boolean(), nullable=True),
        sa.Column("datum_registracije", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_korisnici_id"), "korisnici", ["id"], unique=False)
    op.create_index(op.f("ix_korisnici_email"), "korisnici", ["email"], unique=True)

    op.create_table(
        "parametri",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pol", sa.String(), nullable=True),
        sa.Column("starost", sa.Integer(), nullable=True),
        sa.Column("trudnoca", sa.Boolean(), nullable=True),
        sa.Column("komorbiditeti", sa.Text(), nullable=True),
        sa.Column("alergije", sa.Text(), nullable=True),
        sa.Column("fizioloski_status", sa.Text(), nullable=True),
        sa.Column("nutritivni_status", sa.Text(), nullable=True),
        sa.Column("psiholoski_faktori", sa.Text(), nullable=True),
        sa.Column("zivotni_stil", sa.Text(), nullable=True),
        sa.Column("genetski_faktori", sa.Text(), nullable=True),
        sa.Column("okruzenje", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_parametri_id"), "parametri", ["id"], unique=False)

    op.create_table(
        "preporuke",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("metoda", sa.String(), nullable=True),
        sa.Column("terapija_opis", sa.Text(), nullable=True),
        sa.Column("referenca", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_preporuke_id"), "preporuke", ["id"], unique=False)

    op.create_table(
        "suplementi",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("naziv", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("naziv"),
    )
    op.create_index(op.f("ix_suplementi_id"), "suplementi", ["id"], unique=False)

    # ------- tabele koje sadrže FK-eve na prethodne ------------------------
    op.create_table(
        "istorijat",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("korisnik_id", sa.Integer(), nullable=True),
        sa.Column("parametri_id", sa.Integer(), nullable=True),
        sa.Column("preporuka_id", sa.Integer(), nullable=True),
        sa.Column("datum", sa.DateTime(), nullable=True),
        sa.Column("tip_usluge", sa.String(), nullable=True),
        sa.Column("rezultat_pdf", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["korisnik_id"], ["korisnici.id"]),
        sa.ForeignKeyConstraint(["parametri_id"], ["parametri.id"]),
        sa.ForeignKeyConstraint(["preporuka_id"], ["preporuke.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_istorijat_id"), "istorijat", ["id"], unique=False)

    op.create_table(
        "preporuka_biljke",
        sa.Column("preporuka_id", sa.Integer(), nullable=False),
        sa.Column("biljka_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["preporuka_id"], ["preporuke.id"]),
        sa.ForeignKeyConstraint(["biljka_id"], ["biljke.id"]),
        sa.PrimaryKeyConstraint("preporuka_id", "biljka_id"),
    )

    op.create_table(
        "preporuka_suplementi",
        sa.Column("preporuka_id", sa.Integer(), nullable=False),
        sa.Column("suplemenat_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["preporuka_id"], ["preporuke.id"]),
        sa.ForeignKeyConstraint(["suplemenat_id"], ["suplementi.id"]),
        sa.PrimaryKeyConstraint("preporuka_id", "suplemenat_id"),
    )
    # ----------------------------------------------------------------------

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema – briše sve tabele u ispravnom redosledu."""
    # --- brišemo veze (M:N) tabele prvo jer imaju FK zavisnosti ---
    op.drop_table('preporuka_suplementi')
    op.drop_table('preporuka_biljke')

    # --- zatim one koje sadrže FK ka ostalim tabelama ---
    op.drop_index(op.f('ix_istorijat_id'), table_name='istorijat')
    op.drop_table('istorijat')

    # --- zatim osnovne tabele bez zavisnosti (redosled nije kritičan) ---
    op.drop_index(op.f('ix_suplementi_id'), table_name='suplementi')
    op.drop_table('suplementi')

    op.drop_index(op.f('ix_preporuke_id'), table_name='preporuke')
    op.drop_table('preporuke')

    op.drop_index(op.f('ix_parametri_id'), table_name='parametri')
    op.drop_table('parametri')

    op.drop_index(op.f('ix_korisnici_email'), table_name='korisnici')
    op.drop_index(op.f('ix_korisnici_id'), table_name='korisnici')
    op.drop_table('korisnici')

    op.drop_index(op.f('ix_biljke_id'), table_name='biljke')
    op.drop_table('biljke')

