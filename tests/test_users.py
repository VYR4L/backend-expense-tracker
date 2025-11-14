import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Define ambiente de teste antes de importar
os.environ["TESTING"] = "true"

from main import app
from config import Base, get_db
from models.users import User

# Configura banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override da dependency do banco de dados para usar banco de testes."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override da dependency
app.dependency_overrides[get_db] = override_get_db

# Cria o cliente de teste
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Cria e limpa o banco de dados antes de cada teste."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestUserCreation:
    """Testes para criação de usuários."""

    def test_create_user_success(self):
        """Testa criação de usuário com sucesso."""
        response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert "id" in data
        assert "created_at" in data
        assert "hashed_password" not in data  # Não deve retornar senha

    def test_create_user_password_mismatch(self):
        """Testa erro quando senhas não conferem."""
        response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "SecurePass123!",
                "confirm_password": "DifferentPass123!"
            }
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Passwords do not match"

    def test_create_user_duplicate_email(self):
        """Testa erro ao criar usuário com email duplicado."""
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!"
        }
        
        # Primeiro usuário
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == 201
        
        # Segundo usuário com mesmo email
        response2 = client.post("/users/", json=user_data)
        assert response2.status_code == 400
        assert response2.json()["detail"] == "Email already registered"

    def test_create_user_invalid_email(self):
        """Testa erro com email inválido."""
        response = client.post(
            "/users/",
            json={
                "email": "invalid-email",
                "first_name": "John",
                "last_name": "Doe",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        )
        assert response.status_code == 422  # Validation error

    def test_create_user_missing_fields(self):
        """Testa erro quando faltam campos obrigatórios."""
        response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "first_name": "John"
                # faltam last_name, password, confirm_password
            }
        )
        assert response.status_code == 422


class TestUserUpdate:
    """Testes para atualização de usuários."""

    def test_update_user_success(self):
        """Testa atualização de usuário com sucesso."""
        # Cria usuário
        create_response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        )
        user_id = create_response.json()["id"]
        
        # Atualiza usuário
        update_response = client.put(
            f"/users/{user_id}",
            json={
                "first_name": "Jane",
                "last_name": "Smith"
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["first_name"] == "Jane"
        assert data["last_name"] == "Smith"
        assert data["email"] == "test@example.com"  # Email não mudou

    def test_update_user_password(self):
        """Testa atualização de senha."""
        # Cria usuário
        create_response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "OldPass123!",
                "confirm_password": "OldPass123!"
            }
        )
        user_id = create_response.json()["id"]
        
        # Atualiza senha
        update_response = client.put(
            f"/users/{user_id}",
            json={
                "password": "NewPass123!",
                "confirm_password": "NewPass123!"
            }
        )
        assert update_response.status_code == 200

    def test_update_user_password_mismatch(self):
        """Testa erro quando senhas não conferem na atualização."""
        # Cria usuário
        create_response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "OldPass123!",
                "confirm_password": "OldPass123!"
            }
        )
        user_id = create_response.json()["id"]
        
        # Tenta atualizar com senhas diferentes
        update_response = client.put(
            f"/users/{user_id}",
            json={
                "password": "NewPass123!",
                "confirm_password": "DifferentPass123!"
            }
        )
        assert update_response.status_code == 400
        assert update_response.json()["detail"] == "Passwords do not match"

    def test_update_nonexistent_user(self):
        """Testa erro ao atualizar usuário inexistente."""
        response = client.put(
            "/users/99999",
            json={
                "first_name": "Jane"
            }
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


class TestUserDeletion:
    """Testes para deleção de usuários."""

    def test_delete_user_success(self):
        """Testa deleção de usuário com sucesso."""
        # Cria usuário
        create_response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        )
        user_id = create_response.json()["id"]
        
        # Deleta usuário
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 204

    def test_delete_nonexistent_user(self):
        """Testa erro ao deletar usuário inexistente."""
        response = client.delete("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_user_twice(self):
        """Testa erro ao deletar usuário já deletado."""
        # Cria usuário
        create_response = client.post(
            "/users/",
            json={
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        )
        user_id = create_response.json()["id"]
        
        # Primeira deleção
        delete_response1 = client.delete(f"/users/{user_id}")
        assert delete_response1.status_code == 204
        
        # Segunda deleção
        delete_response2 = client.delete(f"/users/{user_id}")
        assert delete_response2.status_code == 404


class TestHealthEndpoints:
    """Testes para endpoints de saúde da API."""

    def test_root_endpoint(self):
        """Testa endpoint raiz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Expense Tracker API"
        assert data["status"] == "running"

    def test_health_endpoint(self):
        """Testa endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
