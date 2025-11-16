"""Serviço para operações relacionadas a metas (goals)."""
from models.goals import Goal, GoalCreate, GoalOut, GoalUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException


class GoalsService:
    """
    Serviço para operações relacionadas a metas.
    """
    def __init__(self, db: Session):
        self.db = db

    def create_goal(self, goal_create: GoalCreate) -> GoalOut:
        """
        Cria uma nova meta no banco de dados.
        """
        new_goal = Goal(
            user_id=goal_create.user_id,
            name=goal_create.name,
            target_amount=goal_create.target_amount,
            current_amount=goal_create.current_amount or 0.0,
            color=goal_create.color,
            icon=goal_create.icon
        )
        self.db.add(new_goal)
        self.db.commit()
        self.db.refresh(new_goal)
        return GoalOut.model_validate(new_goal)
    
    def get_goal(self, goal_id: int) -> GoalOut:
        """
        Recupera uma meta pelo ID.
        """
        goal = self.db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        return GoalOut.model_validate(goal)
    
    def get_user_goals(self, user_id: int) -> list[GoalOut]:
        """
        Recupera todas as metas de um usuário.
        """
        goals = self.db.query(Goal).filter(
            Goal.user_id == user_id,
            Goal.deleted_at.is_(None)
        ).all()
        return [GoalOut.model_validate(goal) for goal in goals]
    
    def update_goal(self, goal_id: int, goal_update: GoalUpdate) -> GoalOut:
        """
        Atualiza os dados de uma meta existente.
        """
        goal = self.db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        if goal_update.name is not None:
            goal.name = goal_update.name
        
        if goal_update.target_amount is not None:
            goal.target_amount = goal_update.target_amount
        
        if goal_update.current_amount is not None:
            goal.current_amount = goal_update.current_amount
        
        if goal_update.color is not None:
            goal.color = goal_update.color
        
        if goal_update.icon is not None:
            goal.icon = goal_update.icon

        self.db.commit()
        self.db.refresh(goal)
        return GoalOut.model_validate(goal)
    
    def delete_goal(self, goal_id: int) -> None:
        """
        Deleta uma meta do banco de dados (soft delete).
        """
        goal = self.db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        # Soft delete
        from datetime import datetime, timezone
        goal.deleted_at = datetime.now(timezone.utc)
        self.db.commit()

        return None
    
    def add_amount_to_goal(self, goal_id: int, amount: float) -> GoalOut:
        """
        Adiciona um valor ao progresso da meta.
        """
        goal = self.db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        goal.current_amount += amount
        
        # Não permite ultrapassar o target
        if goal.current_amount > goal.target_amount:
            goal.current_amount = goal.target_amount
        
        self.db.commit()
        self.db.refresh(goal)
        return GoalOut.model_validate(goal)
