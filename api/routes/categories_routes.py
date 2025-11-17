"""Rotas relacionadas a categorias."""
from fastapi import APIRouter, Depends, Query
from controllers.categories_controller import CategoriesController
from models.categories import CategoryCreate, CategoryUpdate, CategoryOut
from models.users import User
from sqlalchemy.orm import Session
from config import get_db
from auth import get_current_active_user_dependency


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryOut, status_code=201)
async def create_category(
    category_create: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Cria uma nova categoria.
    """
    return CategoriesController.create_category(category_create=category_create, user_id=current_user.id, db=db)


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Recupera uma categoria pelo ID (apenas do usuário autenticado).
    """
    return CategoriesController.get_category(category_id=category_id, user_id=current_user.id, db=db)


@router.get("/", response_model=list[CategoryOut])
async def get_all_categories(
    category_type: str = Query(None, description="Filtrar por tipo: 'income' ou 'expense'"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Recupera todas as categorias do usuário, opcionalmente filtradas por tipo.
    """
    return CategoriesController.get_all_categories(user_id=current_user.id, category_type=category_type, db=db)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Atualiza uma categoria existente (apenas do usuário autenticado).
    """
    return CategoriesController.update_category(category_id=category_id, user_id=current_user.id, category_update=category_update, db=db)


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Deleta uma categoria (soft delete) do usuário autenticado.
    """
    return CategoriesController.delete_category(category_id=category_id, user_id=current_user.id, db=db)
