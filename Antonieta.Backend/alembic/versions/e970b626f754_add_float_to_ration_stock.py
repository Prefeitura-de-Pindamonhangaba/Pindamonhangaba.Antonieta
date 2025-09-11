"""add float to ration stock

Revision ID: e970b626f754
Revises: 5326baaaf75a
Create Date: 2025-09-10 16:58:15.343624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e970b626f754'
down_revision: Union[str, None] = '5326baaaf75a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: change ration_stock.stock from INTEGER to FLOAT (double precision)."""
    # Use ALTER COLUMN with USING to safely convert existing integer values to double precision.
    op.alter_column(
        'ration_stock',
        'stock',
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using='stock::double precision'
    )


def downgrade() -> None:
    """Downgrade schema: revert ration_stock.stock from FLOAT back to INTEGER."""
    op.alter_column(
        'ration_stock',
        'stock',
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=True,
        postgresql_using='stock::integer'
    )
