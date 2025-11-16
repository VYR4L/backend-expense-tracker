"""Controlador para rotas relacionadas a categorias."""
from fastapi import Depends
from fastapi.responses import Response
from services.categories_service import CategoriesService
from models.categories import CategoryCreate, CategoryUpdate, CategoryOut
from sqlalchemy.orm import Session
from config import get_db


class CategoriesController:
    """
    Controlador para rotas relacionadas a categorias.
    """
    @staticmethod
    def create_category(category_create: CategoryCreate, db: Session = Depends(get_db)) -> CategoryOut:
        """
        Rota para criar uma nova categoria.
        """
        categories_service = CategoriesService(db)
        return categories_service.create_category(category_create)

    @staticmethod
    def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryOut:
        """
        Rota para recuperar uma categoria pelo ID.
        """
        categories_service = CategoriesService(db)
        return categories_service.get_category(category_id)

    @staticmethod
    def get_all_categories(category_type: str = None, db: Session = Depends(get_db)) -> list[CategoryOut]:
        """
        Rota para recuperar todas as categorias.
        """
        categories_service = CategoriesService(db)
        return categories_service.get_all_categories(category_type)

    @staticmethod
    def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)) -> CategoryOut:
        """
        Rota para atualizar uma categoria existente.
        """
        categories_service = CategoriesService(db)
        return categories_service.update_category(category_id, category_update)
    
    @staticmethod
    def delete_category(category_id: int, db: Session = Depends(get_db)) -> Response:
        """
        Rota para deletar uma categoria.
        """
        categories_service = CategoriesService(db)
        categories_service.delete_category(category_id)
        return Response(status_code=204)
