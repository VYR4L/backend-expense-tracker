"""Rotas relacionadas a transações."""
from fastapi import APIRouter, Depends
from controllers.transactions_controller import TransactionsController
from models.transactions import TransactionCreate, TransactionUpdate, TransactionOut
from sqlalchemy.orm import Session
from config import get_db


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/", response_model=TransactionOut, status_code=201)
async def create_transaction(transaction_create: TransactionCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova transação.
    """
    return TransactionsController.create_transaction(transaction_create=transaction_create, db=db)


@router.get("/{transaction_id}", response_model=TransactionOut)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Recupera uma transação pelo ID.
    """
    return TransactionsController.get_transaction(transaction_id=transaction_id, db=db)


@router.get("/", response_model=list[TransactionOut])
async def get_paginated_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Recupera uma lista paginada de transações.
    """
    return TransactionsController.get_paginated_transactions(skip=skip, limit=limit, db=db)


@router.put("/{transaction_id}", response_model=TransactionOut)
async def update_transaction(transaction_id: int, transaction_update: TransactionUpdate, db: Session = Depends(get_db)):
    """
    Atualiza uma transação existente.
    """
    return TransactionsController.update_transaction(transaction_id=transaction_id, transaction_update=transaction_update, db=db)


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma transação.
    """
    return TransactionsController.delete_transaction(transaction_id=transaction_id, db=db)
