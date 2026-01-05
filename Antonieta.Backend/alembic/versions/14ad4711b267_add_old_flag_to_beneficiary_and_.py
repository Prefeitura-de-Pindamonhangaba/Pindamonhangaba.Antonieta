"""add_old_flag_to_beneficiary_and_distribution

Revision ID: 14ad4711b267
Revises: 9c09dd14096d
Create Date: 2026-01-05 15:04:12.284675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14ad4711b267'
down_revision: Union[str, None] = '9c09dd14096d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Adicionar coluna 'old' à tabela beneficiary
    op.add_column('beneficiary', sa.Column('old', sa.Boolean(), nullable=True, comment='Registros anteriores à data de corte'))
    op.create_index(op.f('ix_beneficiary_old'), 'beneficiary', ['old'], unique=False)
    
    # Adicionar coluna 'old' à tabela distribution
    op.add_column('distribution', sa.Column('old', sa.Boolean(), nullable=True, comment='Registros anteriores à data de corte'))
    op.create_index(op.f('ix_distribution_old'), 'distribution', ['old'], unique=False)
    
    # Marcar todos os registros existentes como old=False por padrão
    # Os registros antigos serão marcados posteriormente por um script de migração de dados
    op.execute("UPDATE beneficiary SET old = FALSE WHERE old IS NULL")
    op.execute("UPDATE distribution SET old = FALSE WHERE old IS NULL")
    
    # Tornar as colunas NOT NULL após definir os valores padrão
    op.alter_column('beneficiary', 'old', nullable=False)
    op.alter_column('distribution', 'old', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Remover índices
    op.drop_index(op.f('ix_distribution_old'), table_name='distribution')
    op.drop_index(op.f('ix_beneficiary_old'), table_name='beneficiary')
    
    # Remover colunas
    op.drop_column('distribution', 'old')
    op.drop_column('beneficiary', 'old')
