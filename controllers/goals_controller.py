"""Controlador para rotas relacionadas a metas (goals)."""
from fastapi import Depends
from fastapi.responses import Response
from services.goals_service import GoalsService
from models.goals import GoalCreate, GoalUpdate, GoalOut
from sqlalchemy.orm import Session
from config import get_db


class GoalsController:
    """
    Controlador para rotas relacionadas a metas.
    """
    @staticmethod
    def create_goal(goal_create: GoalCreate, db: Session = Depends(get_db)) -> GoalOut:
        """
        Rota para criar uma nova meta.
        """
        goals_service = GoalsService(db)
        return goals_service.create_goal(goal_create)

    @staticmethod
    def get_goal(goal_id: int, db: Session = Depends(get_db)) -> GoalOut:
        """
        Rota para recuperar uma meta pelo ID.
        """
        goals_service = GoalsService(db)
        return goals_service.get_goal(goal_id)

    @staticmethod
    def get_user_goals(user_id: int, db: Session = Depends(get_db)) -> list[GoalOut]:
        """
        Rota para recuperar todas as metas de um usuário.
        """
        goals_service = GoalsService(db)
        return goals_service.get_user_goals(user_id)

    @staticmethod
    def update_goal(goal_id: int, goal_update: GoalUpdate, db: Session = Depends(get_db)) -> GoalOut:
        """
        Rota para atualizar uma meta existente.
        """
        goals_service = GoalsService(db)
        return goals_service.update_goal(goal_id, goal_update)
    
    @staticmethod
    def delete_goal(goal_id: int, db: Session = Depends(get_db)) -> Response:
        """
        Rota para deletar uma meta.
        """
        goals_service = GoalsService(db)
        goals_service.delete_goal(goal_id)
        return Response(status_code=204)
    
    @staticmethod
    def add_amount_to_goal(goal_id: int, amount: float, db: Session = Depends(get_db)) -> GoalOut:
        """
        Rota para adicionar valor ao progresso da meta.
        """
        goals_service = GoalsService(db)
        return goals_service.add_amount_to_goal(goal_id, amount)
