"""Controlador para rotas relacionadas a balances."""
from fastapi import Depends
from services.balances_service import BalanceService
from models.balances import BalanceOut
from sqlalchemy.orm import Session
from config import get_db


class BalanceController:
    """
    Controlador para rotas relacionadas a balances.
    """
    @staticmethod
    def get_user_balance(user_id: int, db: Session = Depends(get_db)) -> BalanceOut:
        """
        Rota para recuperar o balance de um usuário.
        """
        balance_service = BalanceService(db)
        return balance_service.get_user_balance(user_id)
