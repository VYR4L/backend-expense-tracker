"""Configuração compartilhada para todos os testes."""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Define ambiente de teste antes de importar
os.environ["TESTING"] = "true"

# Importa todos os modelos ANTES de criar o app
from models import users, categories, goals, transactions, balances
from main import app
from config import Base, get_db

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


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Cria e limpa o banco de dados antes de cada teste."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Fixture para criar um usuário de teste."""
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
    return response.json()


@pytest.fixture
def auth_token(test_user):
    """Fixture para obter token JWT de autenticação."""
    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "SecurePass123!"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Fixture para obter headers de autenticação."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def test_category(auth_headers):
    """Fixture para criar uma categoria de teste."""
    response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "category_type": "expense",
            "color": "#FF5722"
        },
        headers=auth_headers
    )
    return response.json()
