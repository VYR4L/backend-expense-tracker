"""Serviço para operações relacionadas a balances."""
from models.balances import Balance, BalanceOut
from sqlalchemy.orm import Session
from fastapi import HTTPException


class BalanceService:
    """
    Serviço para operações relacionadas a balances.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_user_balance(self, user_id: int) -> BalanceOut:
        """
        Recupera o balance de um usuário.
        """
        balance = self.db.query(Balance).filter(Balance.user_id == user_id).first()
        if not balance:
            raise HTTPException(status_code=404, detail="Balance not found for this user")
        
        return BalanceOut.model_validate(balance)
