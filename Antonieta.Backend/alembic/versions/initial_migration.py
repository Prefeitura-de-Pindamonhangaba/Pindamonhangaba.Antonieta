"""initial migration

Revision ID: initial_migration
Create Date: 2024-06-09
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic
revision = '001_initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(), unique=True, index=True),
        sa.Column('hashed_password', sa.String()),
        sa.Column('full_name', sa.String()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=func.now())
    )

    # Create beneficiary table
    op.create_table(
        'beneficiary',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), index=True),
        sa.Column('document', sa.String(), index=True),
        sa.Column('address', sa.String(), index=True),
        sa.Column('contact', sa.String(), index=True),
        sa.Column('monthly_limit', sa.Integer(), default=0)
    )

    # Create ration_stock table
    op.create_table(
        'ration_stock',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), unique=True, index=True),
        sa.Column('description', sa.String(), index=True),
        sa.Column('unit', sa.String(), index=True),
        sa.Column('stock', sa.Integer(), index=True)
    )

    # Create ration_input table
    op.create_table(
        'ration_input',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('ration_stock_id', sa.Integer(), sa.ForeignKey('ration_stock.id'), index=True),
        sa.Column('amount', sa.Integer(), index=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('description', sa.String(), index=True)
    )

    # Create distribution table
    op.create_table(
        'distribution',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('ration_id', sa.Integer(), sa.ForeignKey('ration_stock.id'), index=True),
        sa.Column('beneficiary_id', sa.Integer(), sa.ForeignKey('beneficiary.id'), index=True),
        sa.Column('amount', sa.Integer(), index=True),
        sa.Column('date', sa.DateTime(), nullable=False)
    )

def downgrade():
    # Drop tables in reverse order to respect foreign key constraints
    op.drop_table('distribution')
    op.drop_table('ration_input')
    op.drop_table('ration_stock')
    op.drop_table('beneficiary')
    op.drop_table('users')