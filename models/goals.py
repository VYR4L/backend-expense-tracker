from pydantic import BaseModel, computed_field
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0, nullable=False)
    color = Column(String(7), nullable=False)  # e.g., Hex color code
    icon = Column(String(100), nullable=True)  # e.g., icon name or
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamento
    user = relationship("User", back_populates="goals")


class GoalBase(BaseModel):
    user_id: int
    name: str
    target_amount: float
    current_amount: Optional[float] = 0.0
    color: str  # e.g., Hex color code
    icon: Optional[str] = None  # e.g., icon name or path


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    color: Optional[str] = None  # e.g., Hex color code
    icon: Optional[str] = None  # e.g., icon name or path


class GoalOut(GoalBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @computed_field
    @property
    def percent_complete(self) -> float:
        if self.target_amount == 0:
            return 0.0
        return round((self.current_amount / self.target_amount) * 100, 2)

    model_config = {"from_attributes": True}