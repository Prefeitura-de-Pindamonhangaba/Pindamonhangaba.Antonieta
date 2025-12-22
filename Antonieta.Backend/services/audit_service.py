from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from models.audit_log_model import AuditLog
from models.user_model import User
import json

class AuditService:
    """
    Serviço para gerenciar logs de auditoria
    """
    
    @staticmethod
    def log_action(
        db: Session,
        action: str,
        entity_type: str,
        description: str,
        user: Optional[User] = None,
        entity_id: Optional[int] = None,
        changes: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditLog:
        """
        Registra uma ação no log de auditoria
        
        Args:
            action: Tipo de ação (CREATE, UPDATE, DELETE, LOGIN, etc.)
            entity_type: Tipo de entidade (User, Beneficiary, Distribution, etc.)
            description: Descrição legível da ação
            user: Usuário que executou a ação (opcional)
            entity_id: ID da entidade afetada (opcional)
            changes: Dicionário com mudanças (antes/depois)
            ip_address: IP de origem
            user_agent: Informações do cliente
        """
        audit_log = AuditLog(
            user_id=user.id if user else None,
            user_email=user.email if user else None,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        return audit_log
    
    @staticmethod
    def get_logs(
        db: Session,
        user_id: Optional[int] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        action: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """
        Busca logs de auditoria com filtros
        """
        query = db.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        
        if entity_id:
            query = query.filter(AuditLog.entity_id == entity_id)
        
        if action:
            query = query.filter(AuditLog.action == action)
        
        if start_date:
            query = query.filter(AuditLog.created_at >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.created_at <= end_date)
        
        query = query.order_by(AuditLog.created_at.desc())
        query = query.offset(offset).limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_entity_history(
        db: Session,
        entity_type: str,
        entity_id: int
    ) -> List[AuditLog]:
        """
        Obtém todo o histórico de uma entidade específica
        """
        return db.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        ).order_by(AuditLog.created_at.desc()).all()
    
    @staticmethod
    def get_user_activity(
        db: Session,
        user_id: int,
        days: int = 30
    ) -> List[AuditLog]:
        """
        Obtém a atividade de um usuário nos últimos N dias
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        return db.query(AuditLog).filter(
            AuditLog.user_id == user_id,
            AuditLog.created_at >= start_date
        ).order_by(AuditLog.created_at.desc()).all()
    
    @staticmethod
    def count_logs(
        db: Session,
        user_id: Optional[int] = None,
        entity_type: Optional[str] = None,
        action: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        """
        Conta o número de logs com base nos filtros
        """
        query = db.query(AuditLog)
        
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        
        if action:
            query = query.filter(AuditLog.action == action)
        
        if start_date:
            query = query.filter(AuditLog.created_at >= start_date)
        
        if end_date:
            query = query.filter(AuditLog.created_at <= end_date)
        
        return query.count()
