"""add_audit_system

Revision ID: 96c947e4b10c
Revises: e3ed063862b7
Create Date: 2025-12-22 16:53:50.702236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '96c947e4b10c'
down_revision: Union[str, None] = 'e3ed063862b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - adiciona sistema de auditoria."""
    
    # Criar tabela audit_logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('user_email', sa.String(), nullable=True),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('entity_type', sa.String(length=100), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('changes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_id'), 'audit_logs', ['entity_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_type'), 'audit_logs', ['entity_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    
    # Adicionar campos de auditoria em beneficiary
    op.add_column('beneficiary', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('beneficiary', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.add_column('beneficiary', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('beneficiary', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(None, 'beneficiary', 'users', ['created_by'], ['id'])
    op.create_foreign_key(None, 'beneficiary', 'users', ['updated_by'], ['id'])
    
    # Adicionar campos de auditoria em distribution
    op.add_column('distribution', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('distribution', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.add_column('distribution', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('distribution', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(None, 'distribution', 'users', ['created_by'], ['id'])
    op.create_foreign_key(None, 'distribution', 'users', ['updated_by'], ['id'])
    
    # Adicionar campos de auditoria em ration_input
    op.add_column('ration_input', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('ration_input', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.add_column('ration_input', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('ration_input', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(None, 'ration_input', 'users', ['created_by'], ['id'])
    op.create_foreign_key(None, 'ration_input', 'users', ['updated_by'], ['id'])
    
    # Adicionar campos de auditoria em ration_stock
    op.add_column('ration_stock', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('ration_stock', sa.Column('updated_by', sa.Integer(), nullable=True))
    op.add_column('ration_stock', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('ration_stock', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(None, 'ration_stock', 'users', ['created_by'], ['id'])
    op.create_foreign_key(None, 'ration_stock', 'users', ['updated_by'], ['id'])


def downgrade() -> None:
    """Downgrade schema - remove sistema de auditoria."""
    
    # Remover campos de auditoria de ration_stock
    op.drop_constraint(None, 'ration_stock', type_='foreignkey')
    op.drop_constraint(None, 'ration_stock', type_='foreignkey')
    op.drop_column('ration_stock', 'updated_at')
    op.drop_column('ration_stock', 'updated_by')
    op.drop_column('ration_stock', 'created_at')
    op.drop_column('ration_stock', 'created_by')
    
    # Remover campos de auditoria de ration_input
    op.drop_constraint(None, 'ration_input', type_='foreignkey')
    op.drop_constraint(None, 'ration_input', type_='foreignkey')
    op.drop_column('ration_input', 'updated_at')
    op.drop_column('ration_input', 'updated_by')
    op.drop_column('ration_input', 'created_at')
    op.drop_column('ration_input', 'created_by')
    
    # Remover campos de auditoria de distribution
    op.drop_constraint(None, 'distribution', type_='foreignkey')
    op.drop_constraint(None, 'distribution', type_='foreignkey')
    op.drop_column('distribution', 'updated_at')
    op.drop_column('distribution', 'updated_by')
    op.drop_column('distribution', 'created_at')
    op.drop_column('distribution', 'created_by')
    
    # Remover campos de auditoria de beneficiary
    op.drop_constraint(None, 'beneficiary', type_='foreignkey')
    op.drop_constraint(None, 'beneficiary', type_='foreignkey')
    op.drop_column('beneficiary', 'updated_at')
    op.drop_column('beneficiary', 'updated_by')
    op.drop_column('beneficiary', 'created_at')
    op.drop_column('beneficiary', 'created_by')
    
    # Remover tabela audit_logs
    op.drop_index(op.f('ix_audit_logs_user_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_entity_type'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_entity_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_created_at'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs')
    op.drop_table('audit_logs')
