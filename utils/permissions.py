"""Dependências para proteção de rotas administrativas."""
from fastapi import Header, HTTPException, status
from config import settings
import os


def verify_admin_token(x_admin_token: str = Header(...)):
    """
    Verifica se o token de admin está correto.
    Use esta dependência apenas para rotas administrativas (/health, /config, /docs).
    """
    admin_token = os.getenv("ADMIN_TOKEN", settings.JWT_SECRET_KEY)
    
    if x_admin_token != admin_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin token"
        )
    return True
