"""Testes para rotas de categorias."""
from tests.conftest import client


class TestCategoryCreation:
    """Testes para criação de categorias."""

    def test_create_category_success(self, auth_headers):
        """Testa criação de categoria com sucesso."""
        response = client.post(
            "/categories/",
            json={
                "name": "Salary",
                "category_type": "income",
                "color": "#4CAF50",
                "icon": "money"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Salary"
        assert data["category_type"] == "income"
        assert data["color"] == "#4CAF50"
        assert data["icon"] == "money"
        assert "id" in data
        assert "created_at" in data

    def test_create_category_duplicate_name(self, auth_headers):
        """Testa erro ao criar categoria com nome duplicado."""
        category_data = {
            "name": "Food",
            "category_type": "expense",
            "color": "#FF5722",
            "icon": "restaurant"
        }
        
        # Primeira categoria
        response1 = client.post("/categories/", json=category_data, headers=auth_headers)
        assert response1.status_code == 201
        
        # Segunda categoria com mesmo nome
        response2 = client.post("/categories/", json=category_data, headers=auth_headers)
        assert response2.status_code == 400
        assert response2.json()["detail"] == "Category with this name already exists"

    def test_create_category_missing_fields(self, auth_headers):
        """Testa erro quando faltam campos obrigatórios."""
        response = client.post(
            "/categories/",
            json={
                "name": "Transport"
                # faltam category_type, color
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_category_without_auth(self):
        """Testa erro ao criar categoria sem autenticação."""
        response = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#FF5722"
            }
        )
        assert response.status_code == 401


class TestCategoryRetrieval:
    """Testes para recuperação de categorias."""

    def test_get_category_success(self, auth_headers):
        """Testa busca de categoria por ID."""
        # Cria categoria
        create_response = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#FF5722",
                "icon": "restaurant"
            },
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        # Busca categoria
        get_response = client.get(f"/categories/{category_id}", headers=auth_headers)
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["name"] == "Food"
        assert data["id"] == category_id

    def test_get_category_not_found(self, auth_headers):
        """Testa erro ao buscar categoria inexistente."""
        response = client.get("/categories/99999", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"

    def test_get_all_categories(self, auth_headers):
        """Testa listagem de todas as categorias."""
        # Cria categorias
        client.post("/categories/", json={
            "name": "Salary",
            "category_type": "income",
            "color": "#4CAF50",
            "icon": "money"
        }, headers=auth_headers)
        client.post("/categories/", json={
            "name": "Food",
            "category_type": "expense",
            "color": "#FF5722",
            "icon": "restaurant"
        }, headers=auth_headers)
        
        # Lista todas
        response = client.get("/categories/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_categories_filtered_by_type(self, auth_headers):
        """Testa listagem filtrada por tipo."""
        # Cria categorias
        client.post("/categories/", json={
            "name": "Salary",
            "category_type": "income",
            "color": "#4CAF50"
        }, headers=auth_headers)
        client.post("/categories/", json={
            "name": "Food",
            "category_type": "expense",
            "color": "#FF5722"
        }, headers=auth_headers)
        
        # Filtra por tipo income
        response = client.get("/categories/?category_type=income", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category_type"] == "income"


class TestCategoryUpdate:
    """Testes para atualização de categorias."""

    def test_update_category_success(self, auth_headers):
        """Testa atualização de categoria."""
        # Cria categoria
        create_response = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#FF5722"
            },
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        # Atualiza categoria
        update_response = client.put(
            f"/categories/{category_id}",
            json={
                "name": "Groceries",
                "color": "#FF9800"
            },
            headers=auth_headers
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["name"] == "Groceries"
        assert data["color"] == "#FF9800"

    def test_update_category_not_found(self, auth_headers):
        """Testa erro ao atualizar categoria inexistente."""
        response = client.put(
            "/categories/99999",
            json={"name": "Test"},
            headers=auth_headers
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"


class TestCategoryDeletion:
    """Testes para deleção de categorias."""

    def test_delete_category_success(self, auth_headers):
        """Testa deleção de categoria."""
        # Cria categoria
        create_response = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#FF5722"
            },
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        # Deleta categoria
        delete_response = client.delete(f"/categories/{category_id}", headers=auth_headers)
        assert delete_response.status_code == 204

    def test_delete_category_not_found(self, auth_headers):
        """Testa erro ao deletar categoria inexistente."""
        response = client.delete("/categories/99999", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"


class TestCategoryUserIsolation:
    """Testes para isolamento de categorias entre usuários."""

    def test_users_cannot_see_each_others_categories(self, auth_headers):
        """Testa que usuários não veem categorias de outros usuários."""
        # Usuário 1 cria categoria
        client.post(
            "/categories/",
            json={
                "name": "User1 Category",
                "category_type": "expense",
                "color": "#FF5722"
            },
            headers=auth_headers
        )
        
        # Cria segundo usuário
        client.post(
            "/users/",
            json={
                "email": "user2@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        )
        
        # Login do segundo usuário
        login_response = client.post(
            "/auth/login",
            data={
                "username": "user2@example.com",
                "password": "SecurePass123!"
            }
        )
        user2_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        # Usuário 2 lista categorias - não deve ver categorias do usuário 1
        response = client.get("/categories/", headers=user2_headers)
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_user_cannot_access_another_users_category(self, auth_headers):
        """Testa que usuário não pode acessar categoria de outro usuário."""
        # Usuário 1 cria categoria
        create_response = client.post(
            "/categories/",
            json={
                "name": "User1 Category",
                "category_type": "expense",
                "color": "#FF5722"
            },
            headers=auth_headers
        )
        category_id = create_response.json()["id"]
        
        # Cria segundo usuário
        client.post(
            "/users/",
            json={
                "email": "user2@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        )
        
        # Login do segundo usuário
        login_response = client.post(
            "/auth/login",
            data={
                "username": "user2@example.com",
                "password": "SecurePass123!"
            }
        )
        user2_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        # Usuário 2 tenta acessar categoria do usuário 1
        response = client.get(f"/categories/{category_id}", headers=user2_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"

    def test_user_can_create_category_with_same_name_as_another_user(self, auth_headers):
        """Testa que diferentes usuários podem ter categorias com mesmo nome."""
        # Usuário 1 cria categoria
        response1 = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#FF5722"
            },
            headers=auth_headers
        )
        assert response1.status_code == 201
        
        # Cria segundo usuário
        client.post(
            "/users/",
            json={
                "email": "user2@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        )
        
        # Login do segundo usuário
        login_response = client.post(
            "/auth/login",
            data={
                "username": "user2@example.com",
                "password": "SecurePass123!"
            }
        )
        user2_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        # Usuário 2 cria categoria com mesmo nome - deve funcionar
        response2 = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#4CAF50"
            },
            headers=user2_headers
        )
        assert response2.status_code == 201
        assert response2.json()["name"] == "Food"
