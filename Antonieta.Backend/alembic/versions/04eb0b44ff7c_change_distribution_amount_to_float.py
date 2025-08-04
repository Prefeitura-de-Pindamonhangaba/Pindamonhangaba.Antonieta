"""Change distribution amount to float

Revision ID: 04eb0b44ff7c
Revises: 260395b98da4
Create Date: 2025-08-04 14:26:44.699553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '04eb0b44ff7c'
down_revision: Union[str, None] = '260395b98da4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Alterar o tipo da coluna amount de Integer para Float
    op.alter_column('distribution', 'amount',
                    existing_type=sa.INTEGER(),
                    type_=sa.Float(),
                    existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Reverter o tipo da coluna amount de Float para Integer
    op.alter_column('distribution', 'amount',
                    existing_type=sa.Float(),
                    type_=sa.INTEGER(),
                    existing_nullable=True)
