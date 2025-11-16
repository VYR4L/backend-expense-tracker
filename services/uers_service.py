from models.users import User, UserCreate, UserOut, UserUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException
import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


class UserService:
    """
    Serviço para operações relacionadas a usuários.
    """
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> UserOut:
        """
        Cria um novo usuário no banco de dados.
        """
        if user_create.password != user_create.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        existing_user = self.db.query(User).filter(User.email == user_create.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hash_password(user_create.password)
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return UserOut.model_validate(new_user)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> UserOut:
        """
        Atualiza os dados de um usuário existente.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user_update.first_name is not None:
            user.first_name = user_update.first_name
        if user_update.last_name is not None:
            user.last_name = user_update.last_name
        if user_update.password is not None:
            if user_update.password != user_update.confirm_password:
                raise HTTPException(status_code=400, detail="Passwords do not match")
            user.hashed_password = hash_password(user_update.password)

        self.db.commit()
        self.db.refresh(user)
        return UserOut.model_validate(user)
    
    def delete_user(self, user_id: int) -> None:
        """
        Deleta um usuário do banco de dados.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.db.delete(user)
        self.db.commit()