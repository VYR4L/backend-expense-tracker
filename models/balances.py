from pydantic import BaseModel, computed_field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config import Base


class Balance(Base):
    """
    Tabela para armazenar saldo e estatísticas do usuário.
    Atualizada a cada transação criada/atualizada/deletada.
    """
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Saldo atual (income - expenses)
    current_balance = Column(Float, default=0.0, nullable=False)
    
    # Totais do mês atual
    monthly_income = Column(Float, default=0.0, nullable=False)
    monthly_expenses = Column(Float, default=0.0, nullable=False)
    
    # Total de todas as transações (histórico completo)
    total_income = Column(Float, default=0.0, nullable=False)
    total_expenses = Column(Float, default=0.0, nullable=False)
    
    # Média diária de gastos (para projeção)
    daily_average_expense = Column(Float, default=0.0, nullable=False)
    
    # Timestamps
    last_transaction_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamento
    user = relationship("User", back_populates="balance")


class BalanceBase(BaseModel):
    user_id: int
    current_balance: float
    monthly_income: float
    monthly_expenses: float
    total_income: float
    total_expenses: float
    daily_average_expense: float


class BalanceOut(BalanceBase):
    id: int
    last_transaction_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    @computed_field
    @property
    def monthly_net(self) -> float:
        """Resultado líquido do mês (income - expenses)."""
        return round(self.monthly_income - self.monthly_expenses, 2)
    
    @computed_field
    @property
    def projected_month_end_balance(self) -> float:
        """Projeção de saldo ao fim do mês baseado na média diária."""
        # Calcula dias restantes no mês
        now = datetime.now(timezone.utc)
        days_in_month = 30  # Simplificado, pode usar calendar.monthrange para ser preciso
        day_of_month = now.day
        days_remaining = days_in_month - day_of_month
        
        # Projeção: saldo atual - (média diária * dias restantes)
        projected_expenses = self.daily_average_expense * days_remaining
        return round(self.current_balance - projected_expenses, 2)
    
    @computed_field
    @property
    def total_net(self) -> float:
        """Resultado líquido total (histórico completo)."""
        return round(self.total_income - self.total_expenses, 2)

    model_config = {"from_attributes": True}
