"""add observations to distributions

Revision ID: 793843838bd9
Revises: 746c831787ab
Create Date: 2025-08-07 10:35:35.199856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '793843838bd9'
down_revision: Union[str, None] = '746c831787ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add observations column to distribution table."""
    op.add_column('distribution', sa.Column('observations', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema - Remove observations column from distribution table."""
    op.drop_column('distribution', 'observations')
