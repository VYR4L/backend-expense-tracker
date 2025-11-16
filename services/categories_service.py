"""Serviço para operações relacionadas a categorias."""
from models.categories import Category, CategoryCreate, CategoryOut, CategoryUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException


class CategoriesService:
    """
    Serviço para operações relacionadas a categorias.
    """
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, category_create: CategoryCreate) -> CategoryOut:
        """
        Cria uma nova categoria no banco de dados.
        """
        # Verifica se já existe categoria com o mesmo nome
        existing_category = self.db.query(Category).filter(Category.name == category_create.name).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
        
        new_category = Category(
            name=category_create.name,
            category_type=category_create.category_type,
            color=category_create.color,
            icon=category_create.icon
        )
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return CategoryOut.model_validate(new_category)
    
    def get_category(self, category_id: int) -> CategoryOut:
        """
        Recupera uma categoria pelo ID.
        """
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        return CategoryOut.model_validate(category)
    
    def get_all_categories(self, category_type: str = None) -> list[CategoryOut]:
        """
        Recupera todas as categorias, opcionalmente filtradas por tipo.
        """
        query = self.db.query(Category).filter(Category.deleted_at.is_(None))
        
        if category_type:
            query = query.filter(Category.category_type == category_type)
        
        categories = query.all()
        return [CategoryOut.model_validate(cat) for cat in categories]
    
    def update_category(self, category_id: int, category_update: CategoryUpdate) -> CategoryOut:
        """
        Atualiza os dados de uma categoria existente.
        """
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        if category_update.name is not None:
            # Verifica se o novo nome já existe
            existing = self.db.query(Category).filter(
                Category.name == category_update.name,
                Category.id != category_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Category with this name already exists")
            category.name = category_update.name
        
        if category_update.category_type is not None:
            category.category_type = category_update.category_type
        
        if category_update.color is not None:
            category.color = category_update.color
        
        if category_update.icon is not None:
            category.icon = category_update.icon

        self.db.commit()
        self.db.refresh(category)
        return CategoryOut.model_validate(category)
    
    def delete_category(self, category_id: int) -> None:
        """
        Deleta uma categoria do banco de dados (soft delete).
        """
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Soft delete
        from datetime import datetime, timezone
        category.deleted_at = datetime.now(timezone.utc)
        self.db.commit()

        return None
