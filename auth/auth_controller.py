"""Controlador de autenticação."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.login_service import LoginService
from config import get_db
from models.users import User


# Define o esquema OAuth2 com endpoint de token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthController:
    """
    Controlador para operações de autenticação.
    """
    
    @staticmethod
    def login(form_data: OAuth2PasswordRequestForm, db: Session) -> dict:
        """
        Endpoint de login que retorna um token JWT.
        
        Args:
            form_data: Formulário com username (email) e password
            db: Sessão do banco de dados
            
        Returns:
            Dict com access_token e informações do usuário
        """
        login_service = LoginService(db)
        return login_service.login(form_data.username, form_data.password)
    
    @staticmethod
    def get_current_user(token: str, db: Session) -> User:
        """
        Dependency para obter o usuário autenticado atual.
        
        Args:
            token: Token JWT do header Authorization
            db: Sessão do banco de dados
            
        Returns:
            User object do usuário autenticado
        """
        login_service = LoginService(db)
        return login_service.get_current_user(token)
    
    @staticmethod
    def get_current_active_user(current_user: User) -> User:
        """
        Verifica se o usuário está ativo (não deletado).
        
        Args:
            current_user: Usuário obtido do token
            
        Returns:
            User object se ativo
            
        Raises:
            HTTPException: Se o usuário estiver inativo
        """
        if current_user.deleted_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user


# Dependency para usar em rotas protegidas
def get_current_user_dependency(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency que pode ser usada em qualquer rota para obter o usuário autenticado.
    
    Usage:
        @router.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user_dependency)):
            return {"user": current_user.email}
    """
    return AuthController.get_current_user(token, db)


def get_current_active_user_dependency(
    current_user: User = Depends(get_current_user_dependency)
) -> User:
    """
    Dependency que verifica se o usuário está ativo.
    
    Usage:
        @router.get("/protected")
        def protected_route(current_user: User = Depends(get_current_active_user_dependency)):
            return {"user": current_user.email}
    """
    return AuthController.get_current_active_user(current_user)
