"""Serviço de autenticação e login com JWT."""
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.users import User
from services.uers_service import verify_password
from config import settings


class LoginService:
    """
    Serviço para operações de autenticação e geração de tokens JWT.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = 120  # Tempo de expiração do token em minutos (2 horas)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica um usuário verificando email e senha.
        
        Args:
            email: Email do usuário
            password: Senha em texto plano
            
        Returns:
            User object se autenticado, None caso contrário
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Cria um token JWT de acesso.
        
        Args:
            data: Dados a serem codificados no token (geralmente user_id, email)
            expires_delta: Tempo de expiração customizado (opcional)
            
        Returns:
            Token JWT como string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> dict:
        """
        Verifica e decodifica um token JWT.
        
        Args:
            token: Token JWT a ser verificado
            
        Returns:
            Payload do token decodificado
            
        Raises:
            HTTPException: Se o token for inválido ou expirado
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: int = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            return payload
        except jwt.InvalidTokenError:
            raise credentials_exception
    
    def get_current_user(self, token: str) -> User:
        """
        Obtém o usuário atual baseado no token JWT.
        
        Args:
            token: Token JWT
            
        Returns:
            User object do usuário autenticado
            
        Raises:
            HTTPException: Se o token for inválido ou usuário não existir
        """
        payload = self.verify_token(token)
        user_id: int = payload.get("sub")
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    
    def login(self, email: str, password: str) -> dict:
        """
        Realiza o login do usuário e retorna um token de acesso.
        
        Args:
            email: Email do usuário
            password: Senha em texto plano
            
        Returns:
            Dict com access_token, token_type e informações do usuário
            
        Raises:
            HTTPException: Se as credenciais forem inválidas
        """
        user = self.authenticate_user(email, password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Cria token com user_id e email
        access_token = self.create_access_token(
            data={"sub": user.id, "email": user.email}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }
