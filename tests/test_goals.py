"""Testes para rotas de metas (goals)."""
from tests.conftest import client, test_user


class TestGoalCreation:
    """Testes para criação de metas."""

    def test_create_goal_success(self, test_user):
        """Testa criação de meta com sucesso."""
        response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "Emergency Fund",
                "target_amount": 10000.0,
                "current_amount": 0.0,
                "color": "#4CAF50",
                "icon": "savings"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Emergency Fund"
        assert data["target_amount"] == 10000.0
        assert data["current_amount"] == 0.0
        assert data["percent_complete"] == 0.0
        assert "id" in data
        assert "created_at" in data

    def test_create_goal_with_initial_amount(self, test_user):
        """Testa criação de meta com valor inicial."""
        response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "Vacation",
                "target_amount": 5000.0,
                "current_amount": 1000.0,
                "color": "#2196F3"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["current_amount"] == 1000.0
        assert data["percent_complete"] == 20.0

    def test_create_goal_missing_fields(self, test_user):
        """Testa erro quando faltam campos obrigatórios."""
        response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "Goal Test"
                # faltam target_amount, color
            }
        )
        assert response.status_code == 422


class TestGoalRetrieval:
    """Testes para recuperação de metas."""

    def test_get_goal_success(self, test_user):
        """Testa busca de meta por ID."""
        # Cria meta
        create_response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "New Car",
                "target_amount": 30000.0,
                "current_amount": 5000.0,
                "color": "#FF5722"
            }
        )
        goal_id = create_response.json()["id"]
        
        # Busca meta
        get_response = client.get(f"/goals/{goal_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["name"] == "New Car"
        assert data["id"] == goal_id
        assert data["percent_complete"] == 16.67

    def test_get_goal_not_found(self):
        """Testa erro ao buscar meta inexistente."""
        response = client.get("/goals/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Goal not found"

    def test_get_user_goals(self, test_user):
        """Testa listagem de metas de um usuário."""
        # Cria metas
        client.post("/goals/", json={
            "user_id": test_user["id"],
            "name": "Emergency Fund",
            "target_amount": 10000.0,
            "color": "#4CAF50"
        })
        client.post("/goals/", json={
            "user_id": test_user["id"],
            "name": "Vacation",
            "target_amount": 5000.0,
            "color": "#2196F3"
        })
        
        # Lista metas do usuário
        response = client.get(f"/goals/user/{test_user['id']}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_user_goals_empty(self, test_user):
        """Testa listagem de metas quando usuário não tem metas."""
        response = client.get(f"/goals/user/{test_user['id']}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


class TestGoalUpdate:
    """Testes para atualização de metas."""

    def test_update_goal_success(self, test_user):
        """Testa atualização de meta."""
        # Cria meta
        create_response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "House Down Payment",
                "target_amount": 50000.0,
                "color": "#9C27B0"
            }
        )
        goal_id = create_response.json()["id"]
        
        # Atualiza meta
        update_response = client.put(
            f"/goals/{goal_id}",
            json={
                "name": "Home Purchase",
                "target_amount": 60000.0
            }
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["name"] == "Home Purchase"
        assert data["target_amount"] == 60000.0

    def test_update_goal_current_amount(self, test_user):
        """Testa atualização do valor atual."""
        # Cria meta
        create_response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "Investment",
                "target_amount": 20000.0,
                "current_amount": 5000.0,
                "color": "#FF9800"
            }
        )
        goal_id = create_response.json()["id"]
        
        # Atualiza valor atual
        update_response = client.put(
            f"/goals/{goal_id}",
            json={"current_amount": 8000.0}
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["current_amount"] == 8000.0
        assert data["percent_complete"] == 40.0

    def test_update_goal_not_found(self):
        """Testa erro ao atualizar meta inexistente."""
        response = client.put(
            "/goals/99999",
            json={"name": "Test"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Goal not found"


class TestGoalDeletion:
    """Testes para deleção de metas."""

    def test_delete_goal_success(self, test_user):
        """Testa deleção de meta."""
        # Cria meta
        create_response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "Temporary Goal",
                "target_amount": 1000.0,
                "color": "#607D8B"
            }
        )
        goal_id = create_response.json()["id"]
        
        # Deleta meta
        delete_response = client.delete(f"/goals/{goal_id}")
        assert delete_response.status_code == 204

    def test_delete_goal_not_found(self):
        """Testa erro ao deletar meta inexistente."""
        response = client.delete("/goals/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Goal not found"


class TestGoalAddAmount:
    """Testes para adicionar valor ao progresso da meta."""

    def test_add_amount_success(self, test_user):
        """Testa adição de valor ao progresso."""
        # Cria meta
        create_response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "Laptop Fund",
                "target_amount": 2000.0,
                "current_amount": 500.0,
                "color": "#3F51B5"
            }
        )
        goal_id = create_response.json()["id"]
        
        # Adiciona valor
        add_response = client.patch(
            f"/goals/{goal_id}/add-amount",
            json={"amount": 300.0}
        )
        assert add_response.status_code == 200
        data = add_response.json()
        assert data["current_amount"] == 800.0
        assert data["percent_complete"] == 40.0

    def test_add_amount_exceeds_target(self, test_user):
        """Testa que valor não ultrapassa o target."""
        # Cria meta
        create_response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "Small Goal",
                "target_amount": 1000.0,
                "current_amount": 900.0,
                "color": "#009688"
            }
        )
        goal_id = create_response.json()["id"]
        
        # Adiciona valor que ultrapassaria
        add_response = client.patch(
            f"/goals/{goal_id}/add-amount",
            json={"amount": 500.0}
        )
        assert add_response.status_code == 200
        data = add_response.json()
        assert data["current_amount"] == 1000.0  # Limitado ao target
        assert data["percent_complete"] == 100.0

    def test_add_negative_amount(self, test_user):
        """Testa erro ao adicionar valor negativo."""
        # Cria meta
        create_response = client.post(
            "/goals/",
            json={
                "user_id": test_user["id"],
                "name": "Test Goal",
                "target_amount": 1000.0,
                "color": "#795548"
            }
        )
        goal_id = create_response.json()["id"]
        
        # Tenta adicionar valor negativo
        add_response = client.patch(
            f"/goals/{goal_id}/add-amount",
            json={"amount": -100.0}
        )
        assert add_response.status_code == 400
        assert add_response.json()["detail"] == "Amount must be positive"

    def test_add_amount_goal_not_found(self):
        """Testa erro ao adicionar valor em meta inexistente."""
        response = client.patch(
            "/goals/99999/add-amount",
            json={"amount": 100.0}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Goal not found"
