"""remove monthly limit

Revision ID: 9cfa6ffbc379
Revises: e970b626f754
Create Date: 2025-09-19 15:31:44.790707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9cfa6ffbc379'
down_revision: Union[str, None] = 'e970b626f754'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: remove monthly_limit column from beneficiary table."""
    with op.batch_alter_table('beneficiary') as batch_op:
        batch_op.drop_column('monthly_limit')


def downgrade() -> None:
    """Downgrade schema: re-create monthly_limit column on beneficiary table."""
    with op.batch_alter_table('beneficiary') as batch_op:
        batch_op.add_column(sa.Column('monthly_limit', sa.Float(), nullable=True))
