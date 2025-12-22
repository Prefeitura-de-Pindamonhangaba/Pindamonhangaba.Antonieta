from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db
from models.user_model import User
from models.audit_log_model import AuditLog
from services.auth_service import get_current_user
from services.audit_service import AuditService
from pydantic import BaseModel

router = APIRouter(prefix="/audit", tags=["audit"])


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    user_email: Optional[str]
    action: str
    entity_type: str
    entity_id: Optional[int]
    description: str
    changes: Optional[dict]
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


def check_admin_permission(current_user: User):
    """Verifica se o usuário atual é administrador"""
    if current_user.role != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem acessar os logs de auditoria."
        )


@router.get("/logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    user_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    entity_type: Optional[str] = Query(None, description="Filtrar por tipo de entidade (User, Beneficiary, etc.)"),
    entity_id: Optional[int] = Query(None, description="Filtrar por ID da entidade"),
    action: Optional[str] = Query(None, description="Filtrar por tipo de ação (CREATE, UPDATE, DELETE, LOGIN, etc.)"),
    start_date: Optional[datetime] = Query(None, description="Data inicial (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Data final (ISO format)"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obter logs de auditoria com filtros (apenas para administradores)
    """
    check_admin_permission(current_user)
    
    logs = AuditService.get_logs(
        db=db,
        user_id=user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )
    
    return logs


@router.get("/logs/entity/{entity_type}/{entity_id}", response_model=List[AuditLogResponse])
async def get_entity_history(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obter histórico completo de uma entidade específica (apenas para administradores)
    """
    check_admin_permission(current_user)
    
    logs = AuditService.get_entity_history(
        db=db,
        entity_type=entity_type,
        entity_id=entity_id
    )
    
    return logs


@router.get("/logs/user/{user_id}", response_model=List[AuditLogResponse])
async def get_user_activity(
    user_id: int,
    days: int = Query(30, ge=1, le=365, description="Número de dias de histórico"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obter atividade de um usuário nos últimos N dias (apenas para administradores)
    """
    check_admin_permission(current_user)
    
    logs = AuditService.get_user_activity(
        db=db,
        user_id=user_id,
        days=days
    )
    
    return logs


@router.get("/logs/count")
async def get_audit_logs_count(
    user_id: Optional[int] = Query(None),
    entity_type: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Contar número de logs com base nos filtros (apenas para administradores)
    """
    check_admin_permission(current_user)
    
    count = AuditService.count_logs(
        db=db,
        user_id=user_id,
        entity_type=entity_type,
        action=action,
        start_date=start_date,
        end_date=end_date
    )
    
    return {"count": count}
