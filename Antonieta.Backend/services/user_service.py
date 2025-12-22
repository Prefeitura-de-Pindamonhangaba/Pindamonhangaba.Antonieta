from sqlalchemy.orm import Session
from typing import List, Optional
from models.user_model import User
from dtos.user_dto import UserCreate, UserUpdate
from services.auth_service import get_password_hash

def get_all_users(db: Session) -> List[User]:
    """Obter todos os usuários"""
    return db.query(User).order_by(User.full_name).all()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Obter um usuário por ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Obter um usuário por email"""
    return db.query(User).filter(User.email == email).first()

def create_new_user(db: Session, user: UserCreate) -> User:
    """Criar um novo usuário"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_by_id(db: Session, user_id: int, user: UserUpdate) -> User:
    """Atualizar um usuário existente"""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        if user.email is not None:
            db_user.email = user.email
        if user.full_name is not None:
            db_user.full_name = user.full_name
        if user.password is not None:
            db_user.hashed_password = get_password_hash(user.password)
        
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user_by_id(db: Session, user_id: int) -> bool:
    """Deletar um usuário"""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
