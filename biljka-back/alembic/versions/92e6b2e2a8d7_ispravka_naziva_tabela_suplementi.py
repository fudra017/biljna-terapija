"""Ispravka naziva tabela suplementi

Revision ID: 92e6b2e2a8d7
Revises: 5bf621e52200
Create Date: 2025-06-23 00:24:55.916228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92e6b2e2a8d7'
down_revision: Union[str, None] = '5bf621e52200'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ispravka pogrešnih naziva suplemenata."""
    op.drop_table('preporuka_suplemeti')
    op.drop_table('suplemeti')

    op.create_table('suplementi',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('naziv', sa.String(), nullable=True),
        sa.UniqueConstraint('naziv')
    )
    op.create_index('ix_suplementi_id', 'suplementi', ['id'])

    op.create_table('preporuka_suplementi',
        sa.Column('preporuka_id', sa.Integer(), nullable=False),
        sa.Column('suplemenat_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['preporuka_id'], ['preporuke.id']),
        sa.ForeignKeyConstraint(['suplemenat_id'], ['suplementi.id']),
        sa.PrimaryKeyConstraint('preporuka_id', 'suplemenat_id')
    )



def downgrade() -> None:
    """Vraća stare nazive tabela sa greškom (suplemeti)."""
    op.drop_table('preporuka_suplementi')
    op.drop_index('ix_suplementi_id', table_name='suplementi')
    op.drop_table('suplementi')

    op.create_table('suplemeti',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('naziv', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('naziv')
    )
    op.create_index('ix_suplementi_id', 'suplemeti', ['id'])

    op.create_table('preporuka_suplemeti',
        sa.Column('preporuka_id', sa.Integer(), nullable=False),
        sa.Column('suplemenat_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['preporuka_id'], ['preporuke.id']),
        sa.ForeignKeyConstraint(['suplemenat_id'], ['suplemeti.id']),
        sa.PrimaryKeyConstraint('preporuka_id', 'suplemenat_id')
    )

