from fastapi import APIRouter, Depends
from fastapi.responses import Response
from controllers.user_controller import UserController
from models.users import UserCreate, UserUpdate, UserOut, User
from sqlalchemy.orm import Session
from config import get_db
from auth import get_current_active_user_dependency


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user_create: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    return UserController.create_user(user_create, db)

@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
) -> UserOut:
    return UserController.update_user(user_id, user_update, db)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user_dependency)
) -> Response:
    return UserController.delete_user(user_id, db)
    

