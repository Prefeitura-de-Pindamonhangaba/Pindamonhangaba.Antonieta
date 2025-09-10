"""add float to inputs

Revision ID: 5326baaaf75a
Revises: 793843838bd9
Create Date: 2025-09-10 15:59:22.037506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5326baaaf75a'
down_revision: Union[str, None] = '793843838bd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: change ration_input.amount from integer to float."""
    # Alter column type from INTEGER to FLOAT/DOUBLE PRECISION.
    # For PostgreSQL include a USING clause to ensure safe conversion.
    op.alter_column(
        'ration_input',
        'amount',
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=True,
        postgresql_using='amount::double precision'
    )


def downgrade() -> None:
    """Downgrade schema: revert ration_input.amount from float back to integer."""
    op.alter_column(
        'ration_input',
        'amount',
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=True,
        postgresql_using='amount::integer'
    )
