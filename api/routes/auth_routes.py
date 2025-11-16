"""Rotas de autenticação."""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.auth_controller import AuthController, get_current_active_user_dependency
from config import get_db
from models.users import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de login que retorna um token JWT.
    
    - **username**: Email do usuário
    - **password**: Senha do usuário
    
    Returns:
        - **access_token**: Token JWT para autenticação
        - **token_type**: Tipo do token (bearer)
        - **user**: Informações do usuário logado
    """
    return AuthController.login(form_data, db)


@router.get("/me")
async def read_users_me(
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Retorna informações do usuário autenticado atual.
    
    Requires: Bearer token no header Authorization
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "is_admin": current_user.is_admin
    }
