"""Rotas relacionadas a balances."""
from fastapi import APIRouter, Depends
from controllers.balances_controller import BalanceController
from models.balances import BalanceOut
from models.users import User
from sqlalchemy.orm import Session
from config import get_db
from auth import get_current_active_user_dependency


router = APIRouter(
    prefix="/balances",
    tags=["Balances"]
)


@router.get("/{user_id}", response_model=BalanceOut)
async def get_user_balance(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Recupera o balance de um usuário.
    """
    return BalanceController.get_user_balance(user_id=user_id, db=db)
