from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from models.user_model import User
from services.audit_service import AuditService
from fastapi import Request

class AuditHelper:
    """
    Helper para simplificar o registro de logs de auditoria
    """
    
    @staticmethod
    def get_client_info(request: Request) -> Dict[str, Optional[str]]:
        """
        Extrai informações do cliente da requisição
        """
        return {
            "ip_address": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent")
        }
    
    @staticmethod
    def log_create(
        db: Session,
        request: Request,
        current_user: User,
        entity_type: str,
        entity_id: int,
        entity_data: Dict[str, Any],
        description: str = None
    ):
        """
        Registra criação de entidade
        """
        client_info = AuditHelper.get_client_info(request)
        
        if not description:
            description = f"{entity_type} criado com sucesso"
        
        AuditService.log_action(
            db=db,
            action="CREATE",
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            user=current_user,
            changes={"new": entity_data},
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"]
        )
    
    @staticmethod
    def log_update(
        db: Session,
        request: Request,
        current_user: User,
        entity_type: str,
        entity_id: int,
        old_data: Dict[str, Any],
        new_data: Dict[str, Any],
        description: str = None
    ):
        """
        Registra atualização de entidade
        """
        client_info = AuditHelper.get_client_info(request)
        
        if not description:
            description = f"{entity_type} atualizado"
        
        # Identificar apenas campos que mudaram
        changes = {}
        for key in new_data:
            if key in old_data and old_data[key] != new_data[key]:
                changes[key] = {"old": old_data[key], "new": new_data[key]}
        
        AuditService.log_action(
            db=db,
            action="UPDATE",
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            user=current_user,
            changes=changes,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"]
        )
    
    @staticmethod
    def log_delete(
        db: Session,
        request: Request,
        current_user: User,
        entity_type: str,
        entity_id: int,
        entity_data: Dict[str, Any],
        description: str = None
    ):
        """
        Registra exclusão de entidade
        """
        client_info = AuditHelper.get_client_info(request)
        
        if not description:
            description = f"{entity_type} excluído"
        
        AuditService.log_action(
            db=db,
            action="DELETE",
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            user=current_user,
            changes={"deleted": entity_data},
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"]
        )
    
    @staticmethod
    def log_login(
        db: Session,
        request: Request,
        user: User,
        success: bool = True
    ):
        """
        Registra tentativa de login
        """
        client_info = AuditHelper.get_client_info(request)
        
        action = "LOGIN_SUCCESS" if success else "LOGIN_FAILED"
        description = f"Login {'bem-sucedido' if success else 'falhou'} para {user.email}"
        
        AuditService.log_action(
            db=db,
            action=action,
            entity_type="User",
            entity_id=user.id if success else None,
            description=description,
            user=user if success else None,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"]
        )
