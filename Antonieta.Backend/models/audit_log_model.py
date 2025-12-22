from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base

class AuditLog(Base):
    """
    Tabela de auditoria para rastrear todas as ações no sistema
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Informações do usuário
    user_id = Column(Integer, index=True, nullable=True)  # ID do usuário que fez a ação
    user_email = Column(String, index=True, nullable=True)  # Email para facilitar consultas
    
    # Informações da ação
    action = Column(String, index=True)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT, etc.
    entity_type = Column(String, index=True)  # User, Beneficiary, Distribution, etc.
    entity_id = Column(Integer, index=True, nullable=True)  # ID do registro afetado
    
    # Detalhes da operação
    description = Column(Text)  # Descrição legível da ação
    changes = Column(JSON, nullable=True)  # JSON com os dados antes/depois da mudança
    
    # Informações de contexto
    ip_address = Column(String, nullable=True)  # IP de origem
    user_agent = Column(String, nullable=True)  # Browser/client info
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<AuditLog {self.action} on {self.entity_type} by {self.user_email}>"
