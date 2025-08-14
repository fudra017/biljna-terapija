"""Nova struktura bez pacijenta i terapije

Revision ID: 5bf621e52200
Revises: 2ec46592d87a
Create Date: 2025-06-22 22:35:22.378037
"""

from alembic import op
import sqlalchemy as sa
from typing import Union, Sequence

# Alembic identifikatori
revision: str = "5bf621e52200"
down_revision: Union[str, None] = "2ec46592d87a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ------------------------------------------------------------
# UPGRADE  – primenjuje novu šemu
# ------------------------------------------------------------

def upgrade() -> None:
    """Kreiraj nove tabele 'suplementi' i 'preporuka_suplementi'."""
    # --- osnovna tabela -------------------------------------------------
    op.create_table(
        "suplementi",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("naziv", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("naziv"),
    )
    op.create_index(op.f("ix_suplementi_id"), "suplementi", ["id"], unique=False)

    # --- many-to-many veza prema 'preporuke' ----------------------------
    op.create_table(
        "preporuka_suplementi",
        sa.Column("preporuka_id", sa.Integer(), nullable=False),
        sa.Column("suplemenat_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["preporuka_id"], ["preporuke.id"]),
        sa.ForeignKeyConstraint(["suplemenat_id"], ["suplementi.id"]),
        sa.PrimaryKeyConstraint("preporuka_id", "suplemenat_id"),
    )
 
    # ### end Alembic commands ###

def downgrade() -> None:
    """Downgrade schema."""
    # --- kreiraj osnovnu tabelu ---
    op.create_table(
        "suplementi",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("naziv", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("suplementi_pkey")),
        sa.UniqueConstraint("naziv", name=op.f("suplementi_naziv_key")),
    )
    op.create_index(op.f("ix_suplementi_id"), "suplementi", ["id"], unique=False)

    # --- tek potom many-to-many tabelu koja referencira suplementi ---
    op.create_table(
        "preporuka_suplementi",
        sa.Column("preporuka_id", sa.INTEGER(), nullable=False),
        sa.Column("suplemenat_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["preporuka_id"], ["preporuke.id"],
            name=op.f("preporuka_suplementi_preporuka_id_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["suplemenat_id"], ["suplementi.id"],
            name=op.f("preporuka_suplementi_suplemenat_id_fkey"),
        ),
        sa.PrimaryKeyConstraint(
            "preporuka_id", "suplemenat_id",
            name=op.f("preporuka_suplementi_pkey"),
        ),
    )

