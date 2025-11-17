from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(50), nullable=False)  # e.g., 'income' or 'expense'
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    date = Column(DateTime, nullable=False)  # Data em que a transação realmente ocorreu
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="transactions")
    category_rel = relationship("Category", back_populates="transactions")


class TransactionBase(BaseModel):
    description: str
    amount: float
    transaction_type: str  # e.g., 'income' or 'expense'
    category_id: int
    date: datetime  # Data em que a transação ocorreu


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    transaction_type: Optional[str] = None  # e.g., 'income' or 'expense'
    category_id: Optional[int] = None
    date: Optional[datetime] = None


class TransactionOut(TransactionBase):
    id: int
    user_id: int
    description: str
    amount: float
    transaction_type: str
    date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PaginatedTransactionResponse(BaseModel):
    items: list[TransactionOut]
    total: int
    page: int
    limit: int