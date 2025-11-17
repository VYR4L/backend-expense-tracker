from models.transactions import Transaction, TransactionCreate, TransactionOut, TransactionUpdate
from models.balances import Balance
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from datetime import datetime, timezone


class TransactionsService:
    """
    Serviço para operações relacionadas a transações.
    """
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, transaction_create: TransactionCreate, user_id: int) -> TransactionOut:
        """
        Cria uma nova transação no banco de dados e atualiza o balance.
        """
        new_transaction = Transaction(
            user_id=user_id,
            description=transaction_create.description,
            amount=transaction_create.amount,
            transaction_type=transaction_create.transaction_type,
            category_id=transaction_create.category_id,
            date=transaction_create.date
        )
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        
        # Atualiza balance do usuário
        self._update_balance(user_id)
        
        return TransactionOut.model_validate(new_transaction)
    
    def _update_balance(self, user_id: int):
        """
        Atualiza o balance do usuário com base em todas as transações.
        """
        # Busca ou cria balance
        balance = self.db.query(Balance).filter(Balance.user_id == user_id).first()
        if not balance:
            balance = Balance(user_id=user_id)
            self.db.add(balance)
        
        # Calcula totais gerais (todas as transações)
        total_income = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "income",
            Transaction.deleted_at.is_(None)
        ).scalar() or 0.0
        
        total_expenses = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "expense",
            Transaction.deleted_at.is_(None)
        ).scalar() or 0.0
        
        # Calcula totais do mês atual
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        monthly_income = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "income",
            Transaction.created_at >= month_start,
            Transaction.deleted_at.is_(None)
        ).scalar() or 0.0
        
        monthly_expenses = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "expense",
            Transaction.created_at >= month_start,
            Transaction.deleted_at.is_(None)
        ).scalar() or 0.0
        
        # Calcula média diária de gastos do mês
        days_in_month = now.day
        daily_average_expense = monthly_expenses / days_in_month if days_in_month > 0 else 0.0
        
        # Última transação
        last_transaction = self.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.deleted_at.is_(None)
        ).order_by(Transaction.created_at.desc()).first()
        
        # Atualiza balance
        balance.current_balance = total_income - total_expenses
        balance.total_income = total_income
        balance.total_expenses = total_expenses
        balance.monthly_income = monthly_income
        balance.monthly_expenses = monthly_expenses
        balance.daily_average_expense = daily_average_expense
        balance.last_transaction_date = last_transaction.created_at if last_transaction else None
        
        self.db.commit()

    
    def get_transaction(self, transaction_id: int, user_id: int) -> TransactionOut:
        """
        Recupera uma transação pelo ID (apenas do usuário autenticado).
        """
        transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return TransactionOut.model_validate(transaction)
    
    def get_paginated_transactions(self, skip: int = 0, limit: int = 10, user_id: int = None) -> list[TransactionOut]:
        """
        Recupera uma lista paginada de transações do usuário.
        """
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        transactions = query.offset(skip).limit(limit).all()
        return [TransactionOut.model_validate(tx) for tx in transactions]
    
    def update_transaction(self, transaction_id: int, user_id: int, transaction_update: TransactionUpdate) -> TransactionOut:
        """
        Atualiza os dados de uma transação existente e recalcula o balance (apenas do usuário autenticado).
        """
        transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        user_id = transaction.user_id

        if transaction_update.description is not None:
            transaction.description = transaction_update.description
        
        if transaction_update.amount is not None:
            transaction.amount = transaction_update.amount
        
        if transaction_update.transaction_type is not None:
            transaction.transaction_type = transaction_update.transaction_type
        
        if transaction_update.category_id is not None:
            transaction.category_id = transaction_update.category_id
        
        if transaction_update.date is not None:
            transaction.date = transaction_update.date

        self.db.commit()
        self.db.refresh(transaction)
        
        # Atualiza balance do usuário
        self._update_balance(user_id)
        
        return TransactionOut.model_validate(transaction)
    
    def delete_transaction(self, transaction_id: int, user_id: int) -> None:
        """
        Deleta uma transação do banco de dados e recalcula o balance (apenas do usuário autenticado).
        """
        transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        ).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        user_id = transaction.user_id
        
        self.db.delete(transaction)
        self.db.commit()
        
        # Atualiza balance do usuário
        self._update_balance(user_id)

        return None
    