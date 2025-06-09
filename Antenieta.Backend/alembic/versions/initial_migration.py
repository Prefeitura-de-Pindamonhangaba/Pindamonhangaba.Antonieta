"""initial migration

Revision ID: 001_initial_migration
Revises: 
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
    # ...existing code...

def downgrade():
    # ...existing code...