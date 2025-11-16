"""Módulo de autenticação."""
from .auth_controller import (
    AuthController,
    get_current_user_dependency,
    get_current_active_user_dependency,
    oauth2_scheme
)
from .login_service import LoginService

__all__ = [
    "AuthController",
    "LoginService",
    "get_current_user_dependency",
    "get_current_active_user_dependency",
    "oauth2_scheme"
]
