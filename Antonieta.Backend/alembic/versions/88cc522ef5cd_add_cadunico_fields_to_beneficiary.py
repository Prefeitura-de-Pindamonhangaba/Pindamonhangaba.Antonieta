"""add_cadunico_fields_to_beneficiary

Revision ID: 88cc522ef5cd
Revises: 9cfa6ffbc379
Create Date: 2025-12-19 15:08:00.425716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88cc522ef5cd'
down_revision: Union[str, None] = '9cfa6ffbc379'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('beneficiary', sa.Column('cadunico_code', sa.String(), nullable=True, comment='Código familiar do CadÚnico'))
    op.add_column('beneficiary', sa.Column('income_range', sa.String(), nullable=True, comment='Faixa de renda familiar per capita'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('beneficiary', 'income_range')
    op.drop_column('beneficiary', 'cadunico_code')
