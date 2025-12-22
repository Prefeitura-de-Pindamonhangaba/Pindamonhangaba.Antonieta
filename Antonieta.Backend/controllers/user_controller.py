from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dtos.user_dto import UserCreate, UserResponse, UserUpdate
from models.user_model import User
from services.auth_service import get_current_user
from services.user_service import (
    get_all_users,
    get_user_by_id,
    create_new_user,
    update_user_by_id,
    delete_user_by_id,
    get_user_by_email
)
from services.audit_helper import AuditHelper

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar todos os usuários"""
    return get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter um usuário específico"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

@router.post("/", response_model=UserResponse)
async def create_user(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Criar um novo usuário (migrado de /auth/register)"""
    # Verificar se o email já existe
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está registrado"
        )
    
    new_user = create_new_user(db, user)
    
    # Registrar criação
    AuditHelper.log_create(
        db=db,
        request=request,
        current_user=current_user,
        entity_type="User",
        entity_id=new_user.id,
        entity_data={"email": new_user.email, "full_name": new_user.full_name, "role": new_user.role},
        description=f"Usuário {new_user.email} criado"
    )
    
    return new_user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: Request,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar um usuário existente"""
    # Verificar se o usuário existe
    existing_user = get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Capturar dados antigos
    old_data = {
        "email": existing_user.email,
        "full_name": existing_user.full_name,
        "role": existing_user.role
    }
    
    # Se o email está sendo alterado, verificar se já existe
    if user.email and user.email != existing_user.email:
        email_exists = get_user_by_email(db, user.email)
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está registrado"
            )
    
    updated_user = update_user_by_id(db, user_id, user)
    
    # Registrar atualização
    new_data = {
        "email": updated_user.email,
        "full_name": updated_user.full_name,
        "role": updated_user.role
    }
    
    AuditHelper.log_update(
        db=db,
        request=request,
        current_user=current_user,
        entity_type="User",
        entity_id=user_id,
        old_data=old_data,
        new_data=new_data,
        description=f"Usuário {updated_user.email} atualizado"
    )
    
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletar um usuário"""
    # Não permitir que o usuário delete a si mesmo
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode deletar seu próprio usuário"
        )
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Registrar exclusão antes de deletar
    AuditHelper.log_delete(
        db=db,
        request=request,
        current_user=current_user,
        entity_type="User",
        entity_id=user_id,
        entity_data={"email": user.email, "full_name": user.full_name, "role": user.role},
        description=f"Usuário {user.email} excluído"
    )
    
    delete_user_by_id(db, user_id)
    return None
