"""add_receives_bpc_loas_to_beneficiary

Revision ID: 9c09dd14096d
Revises: 96c947e4b10c
Create Date: 2025-12-23 14:47:57.665021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c09dd14096d'
down_revision: Union[str, None] = '96c947e4b10c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Adicionar coluna receives_bpc_loas à tabela beneficiary
    op.add_column('beneficiary', sa.Column('receives_bpc_loas', sa.Boolean(), nullable=False, server_default='false', comment='Recebe BPC/LOAS (Benefício de Prestação Continuada)'))


def downgrade() -> None:
    """Downgrade schema."""
    # Remover coluna receives_bpc_loas da tabela beneficiary
    op.drop_column('beneficiary', 'receives_bpc_loas')
