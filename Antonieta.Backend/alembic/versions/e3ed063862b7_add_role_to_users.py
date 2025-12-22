"""add_role_to_users

Revision ID: e3ed063862b7
Revises: 88cc522ef5cd
Create Date: 2025-12-22 16:13:48.005849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3ed063862b7'
down_revision: Union[str, None] = '88cc522ef5cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Adicionar coluna role com valor nullable inicialmente
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    
    # Atualizar registros existentes para ter role="comum"
    op.execute("UPDATE users SET role = 'comum' WHERE role IS NULL")
    
    # Tornar a coluna não nula com valor padrão
    op.alter_column('users', 'role',
                    existing_type=sa.String(),
                    nullable=False,
                    server_default='comum')


def downgrade() -> None:
    """Downgrade schema."""
    # Remover coluna role
    op.drop_column('users', 'role')
