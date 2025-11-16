"""Rotas relacionadas a metas (goals)."""
from fastapi import APIRouter, Depends, Body
from controllers.goals_controller import GoalsController
from models.goals import GoalCreate, GoalUpdate, GoalOut
from models.users import User
from sqlalchemy.orm import Session
from config import get_db
from auth import get_current_active_user_dependency


router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)


@router.post("/", response_model=GoalOut, status_code=201)
async def create_goal(
    goal_create: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Cria uma nova meta.
    """
    return GoalsController.create_goal(goal_create=goal_create, db=db)


@router.get("/{goal_id}", response_model=GoalOut)
async def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Recupera uma meta pelo ID.
    """
    return GoalsController.get_goal(goal_id=goal_id, db=db)


@router.get("/user/{user_id}", response_model=list[GoalOut])
async def get_user_goals(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Recupera todas as metas de um usuário.
    """
    return GoalsController.get_user_goals(user_id=user_id, db=db)


@router.put("/{goal_id}", response_model=GoalOut)
async def update_goal(
    goal_id: int,
    goal_update: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Atualiza uma meta existente.
    """
    return GoalsController.update_goal(goal_id=goal_id, goal_update=goal_update, db=db)


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Deleta uma meta (soft delete).
    """
    return GoalsController.delete_goal(goal_id=goal_id, db=db)


@router.patch("/{goal_id}/add-amount", response_model=GoalOut)
async def add_amount_to_goal(
    goal_id: int,
    amount: float = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
):
    """
    Adiciona um valor ao progresso da meta.
    """
    return GoalsController.add_amount_to_goal(goal_id=goal_id, amount=amount, db=db)
