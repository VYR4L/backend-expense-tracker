"""Testes para rotas de categorias."""
from tests.conftest import client


class TestCategoryCreation:
    """Testes para criação de categorias."""

    def test_create_category_success(self):
        """Testa criação de categoria com sucesso."""
        response = client.post(
            "/categories/",
            json={
                "name": "Salary",
                "category_type": "income",
                "color": "#4CAF50",
                "icon": "money"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Salary"
        assert data["category_type"] == "income"
        assert data["color"] == "#4CAF50"
        assert data["icon"] == "money"
        assert "id" in data
        assert "created_at" in data

    def test_create_category_duplicate_name(self):
        """Testa erro ao criar categoria com nome duplicado."""
        category_data = {
            "name": "Food",
            "category_type": "expense",
            "color": "#FF5722",
            "icon": "restaurant"
        }
        
        # Primeira categoria
        response1 = client.post("/categories/", json=category_data)
        assert response1.status_code == 201
        
        # Segunda categoria com mesmo nome
        response2 = client.post("/categories/", json=category_data)
        assert response2.status_code == 400
        assert response2.json()["detail"] == "Category with this name already exists"

    def test_create_category_missing_fields(self):
        """Testa erro quando faltam campos obrigatórios."""
        response = client.post(
            "/categories/",
            json={
                "name": "Transport"
                # faltam category_type, color
            }
        )
        assert response.status_code == 422


class TestCategoryRetrieval:
    """Testes para recuperação de categorias."""

    def test_get_category_success(self):
        """Testa busca de categoria por ID."""
        # Cria categoria
        create_response = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#FF5722",
                "icon": "restaurant"
            }
        )
        category_id = create_response.json()["id"]
        
        # Busca categoria
        get_response = client.get(f"/categories/{category_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["name"] == "Food"
        assert data["id"] == category_id

    def test_get_category_not_found(self):
        """Testa erro ao buscar categoria inexistente."""
        response = client.get("/categories/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"

    def test_get_all_categories(self):
        """Testa listagem de todas as categorias."""
        # Cria categorias
        client.post("/categories/", json={
            "name": "Salary",
            "category_type": "income",
            "color": "#4CAF50",
            "icon": "money"
        })
        client.post("/categories/", json={
            "name": "Food",
            "category_type": "expense",
            "color": "#FF5722",
            "icon": "restaurant"
        })
        
        # Lista todas
        response = client.get("/categories/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_categories_filtered_by_type(self):
        """Testa listagem filtrada por tipo."""
        # Cria categorias
        client.post("/categories/", json={
            "name": "Salary",
            "category_type": "income",
            "color": "#4CAF50"
        })
        client.post("/categories/", json={
            "name": "Food",
            "category_type": "expense",
            "color": "#FF5722"
        })
        
        # Filtra por tipo income
        response = client.get("/categories/?category_type=income")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category_type"] == "income"


class TestCategoryUpdate:
    """Testes para atualização de categorias."""

    def test_update_category_success(self):
        """Testa atualização de categoria."""
        # Cria categoria
        create_response = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#FF5722"
            }
        )
        category_id = create_response.json()["id"]
        
        # Atualiza categoria
        update_response = client.put(
            f"/categories/{category_id}",
            json={
                "name": "Groceries",
                "color": "#FF9800"
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["name"] == "Groceries"
        assert data["color"] == "#FF9800"

    def test_update_category_not_found(self):
        """Testa erro ao atualizar categoria inexistente."""
        response = client.put(
            "/categories/99999",
            json={"name": "Test"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"


class TestCategoryDeletion:
    """Testes para deleção de categorias."""

    def test_delete_category_success(self):
        """Testa deleção de categoria."""
        # Cria categoria
        create_response = client.post(
            "/categories/",
            json={
                "name": "Food",
                "category_type": "expense",
                "color": "#FF5722"
            }
        )
        category_id = create_response.json()["id"]
        
        # Deleta categoria
        delete_response = client.delete(f"/categories/{category_id}")
        assert delete_response.status_code == 204

    def test_delete_category_not_found(self):
        """Testa erro ao deletar categoria inexistente."""
        response = client.delete("/categories/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"
