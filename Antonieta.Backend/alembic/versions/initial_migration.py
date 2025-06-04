"""Initial migration

Revision ID: f4390a6d4200
Revises: 
Create Date: 2024-03-06 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'f4390a6d4200'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add monthly_limit column to existing beneficiary table
    op.add_column('beneficiary', sa.Column('monthly_limit', sa.Integer(), nullable=True, server_default='0'))

def downgrade() -> None:
    # Remove the monthly_limit column if we need to rollback
    op.drop_column('beneficiary', 'monthly_limit')