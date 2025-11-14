from fastapi import Depends
from fastapi.responses import Response
from services.uers_service import UserService
from models.users import UserCreate, UserUpdate, UserOut
from sqlalchemy.orm import Session
from config import get_db


class UserController:
    """
    Controlador para rotas relacionadas a usuários.
    """
    @staticmethod
    def create_user(user_create: UserCreate, db: Session = Depends(get_db)) -> UserOut:
        """
        Rota para criar um novo usuário.
        """
        user_service = UserService(db)
        return user_service.create_user(user_create)

    @staticmethod
    def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)) -> UserOut:
        """
        Rota para atualizar um usuário existente.
        """
        user_service = UserService(db)
        return user_service.update_user(user_id, user_update)

    @staticmethod
    def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response:
        """
        Rota para deletar um usuário.
        """
        user_service = UserService(db)
        user_service.delete_user(user_id)
        return Response(status_code=204)
    