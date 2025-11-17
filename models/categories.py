from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    category_type = Column(String(50), nullable=False)  # e.g., 'income' or 'expense'
    color = Column(String(7), nullable=False)  # e.g., Hex color code
    icon = Column(String(100), nullable=True)  # e.g., icon name or path
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)

    # Relacionamentos
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category_rel")


class CategoryBase(BaseModel):
    name: str
    category_type: str  # e.g., 'income' or 'expense'
    color: str  # e.g., Hex color code
    icon: Optional[str] = None  # e.g., icon name or path


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    category_type: Optional[str] = None  # e.g., 'income' or 'expense'
    color: Optional[str] = None  # e.g., Hex color code
    icon: Optional[str] = None  # e.g., icon name or path


class CategoryOut(CategoryBase):
    id: int
    name: str
    category_type: str
    color: str
    icon: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}