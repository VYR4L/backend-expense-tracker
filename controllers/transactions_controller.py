from fastapi import Depends
from fastapi.responses import Response
from services.transactions_service import TransactionsService
from models.transactions import TransactionCreate, TransactionUpdate, TransactionOut
from sqlalchemy.orm import Session
from config import get_db


class TransactionsController:
    """
    Controlador para rotas relacionadas a transações.
    """
    @staticmethod
    def create_transaction(transaction_create: TransactionCreate, user_id: int, db: Session = Depends(get_db)) -> TransactionOut:
        """
        Rota para criar uma nova transação.
        """
        transactions_service = TransactionsService(db)
        return transactions_service.create_transaction(transaction_create, user_id)

    @staticmethod
    def get_transaction(transaction_id: int, user_id: int, db: Session = Depends(get_db)) -> TransactionOut:
        """
        Rota para recuperar uma transação pelo ID.
        """
        transactions_service = TransactionsService(db)
        return transactions_service.get_transaction(transaction_id, user_id)

    @staticmethod
    def get_paginated_transactions(skip: int = 0, limit: int = 10, user_id: int = None, db: Session = Depends(get_db)) -> list[TransactionOut]:
        """
        Rota para recuperar uma lista paginada de transações do usuário.
        """
        transactions_service = TransactionsService(db)
        return transactions_service.get_paginated_transactions(skip, limit, user_id)

    @staticmethod
    def update_transaction(transaction_id: int, user_id: int, transaction_update: TransactionUpdate, db: Session = Depends(get_db)) -> TransactionOut:
        """
        Rota para atualizar uma transação existente.
        """
        transactions_service = TransactionsService(db)
        return transactions_service.update_transaction(transaction_id, user_id, transaction_update)
    
    @staticmethod
    def delete_transaction(transaction_id: int, user_id: int, db: Session = Depends(get_db)) -> Response:
        """
        Rota para deletar uma transação.
        """
        transactions_service = TransactionsService(db)
        transactions_service.delete_transaction(transaction_id, user_id)
        return Response(status_code=204)