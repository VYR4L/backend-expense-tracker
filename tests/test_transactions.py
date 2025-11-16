"""Testes para rotas de transações."""
from tests.conftest import client, test_user, test_category


class TestTransactionCreation:
    """Testes para criação de transações."""

    def test_create_transaction_success(self, test_user, test_category, auth_headers):
        """Testa criação de transação com sucesso."""
        response = client.post(
            "/transactions/",
            json={
                "user_id": test_user["id"],
                "description": "Grocery shopping",
                "amount": 150.50,
                "transaction_type": "expense",
                "category_id": test_category["id"]
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Grocery shopping"
        assert data["amount"] == 150.50
        assert data["transaction_type"] == "expense"
        assert "id" in data
        assert "created_at" in data

    def test_create_income_transaction(self, test_user, test_category, auth_headers):
        """Testa criação de transação de entrada."""
        response = client.post(
            "/transactions/",
            json={
                "user_id": test_user["id"],
                "description": "Monthly Salary",
                "amount": 5000.00,
                "transaction_type": "income",
                "category_id": test_category["id"]
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["transaction_type"] == "income"
        assert data["amount"] == 5000.00

    def test_create_transaction_missing_fields(self, test_user, auth_headers):
        """Testa erro quando faltam campos obrigatórios."""
        response = client.post(
            "/transactions/",
            json={
                "user_id": test_user["id"],
                "description": "Test"
                # faltam amount, transaction_type, category_id
            },
            headers=auth_headers
        )
        assert response.status_code == 422


class TestTransactionRetrieval:
    """Testes para recuperação de transações."""

    def test_get_transaction_success(self, test_user, test_category, auth_headers):
        """Testa busca de transação por ID."""
        # Cria transação
        create_response = client.post(
            "/transactions/",
            json={
                "user_id": test_user["id"],
                "description": "Coffee",
                "amount": 5.50,
                "transaction_type": "expense",
                "category_id": test_category["id"]
            },
            headers=auth_headers
        )
        transaction_id = create_response.json()["id"]
        
        # Busca transação
        get_response = client.get(f"/transactions/{transaction_id}", headers=auth_headers)
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["description"] == "Coffee"
        assert data["id"] == transaction_id

    def test_get_transaction_not_found(self, auth_headers):
        """Testa erro ao buscar transação inexistente."""
        response = client.get("/transactions/99999", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Transaction not found"

    def test_get_paginated_transactions(self, test_user, test_category, auth_headers):
        """Testa listagem paginada de transações."""
        # Cria múltiplas transações
        for i in range(5):
            client.post("/transactions/", json={
                "user_id": test_user["id"],
                "description": f"Transaction {i}",
                "amount": 10.0 * (i + 1),
                "transaction_type": "expense",
                "category_id": test_category["id"]
            }, headers=auth_headers)
        
        # Lista com limite
        response = client.get("/transactions/?skip=0&limit=3", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_get_empty_transactions(self, auth_headers):
        """Testa listagem quando não há transações."""
        response = client.get("/transactions/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


class TestTransactionUpdate:
    """Testes para atualização de transações."""

    def test_update_transaction_success(self, test_user, test_category, auth_headers):
        """Testa atualização de transação."""
        # Cria transação
        create_response = client.post(
            "/transactions/",
            json={
                "user_id": test_user["id"],
                "description": "Restaurant",
                "amount": 50.00,
                "transaction_type": "expense",
                "category_id": test_category["id"]
            },
            headers=auth_headers
        )
        transaction_id = create_response.json()["id"]
        
        # Atualiza transação
        update_response = client.put(
            f"/transactions/{transaction_id}",
            json={
                "description": "Fine Dining",
                "amount": 75.00
            },
            headers=auth_headers
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["description"] == "Fine Dining"
        assert data["amount"] == 75.00

    def test_update_transaction_type(self, test_user, test_category, auth_headers):
        """Testa atualização do tipo de transação."""
        # Cria transação
        create_response = client.post(
            "/transactions/",
            json={
                "user_id": test_user["id"],
                "description": "Money",
                "amount": 100.00,
                "transaction_type": "expense",
                "category_id": test_category["id"]
            },
            headers=auth_headers
        )
        transaction_id = create_response.json()["id"]
        
        # Muda tipo
        update_response = client.put(
            f"/transactions/{transaction_id}",
            json={"transaction_type": "income"},
            headers=auth_headers
        )
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["transaction_type"] == "income"

    def test_update_transaction_not_found(self, auth_headers):
        """Testa erro ao atualizar transação inexistente."""
        response = client.put(
            "/transactions/99999",
            json={"description": "Test"},
            headers=auth_headers
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Transaction not found"


class TestTransactionDeletion:
    """Testes para deleção de transações."""

    def test_delete_transaction_success(self, test_user, test_category, auth_headers):
        """Testa deleção de transação."""
        # Cria transação
        create_response = client.post(
            "/transactions/",
            json={
                "user_id": test_user["id"],
                "description": "Temporary",
                "amount": 10.00,
                "transaction_type": "expense",
                "category_id": test_category["id"]
            },
            headers=auth_headers
        )
        transaction_id = create_response.json()["id"]
        
        # Deleta transação
        delete_response = client.delete(f"/transactions/{transaction_id}", headers=auth_headers)
        assert delete_response.status_code == 204

    def test_delete_transaction_not_found(self, auth_headers):
        """Testa erro ao deletar transação inexistente."""
        response = client.delete("/transactions/99999", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Transaction not found"


class TestBalanceUpdates:
    """Testes para verificar atualização automática do balance."""

    def test_balance_updates_on_transaction_creation(self, test_user, test_category, auth_headers):
        """Testa se balance é criado/atualizado ao criar transação."""
        # Cria transação de entrada
        client.post("/transactions/", json={
            "user_id": test_user["id"],
            "description": "Salary",
            "amount": 5000.00,
            "transaction_type": "income",
            "category_id": test_category["id"]
        }, headers=auth_headers)
        
        # Cria transação de saída
        client.post("/transactions/", json={
            "user_id": test_user["id"],
            "description": "Rent",
            "amount": 1500.00,
            "transaction_type": "expense",
            "category_id": test_category["id"]
        }, headers=auth_headers)
        
        # Verifica balance
        balance_response = client.get(f"/balances/{test_user['id']}", headers=auth_headers)
        assert balance_response.status_code == 200
        balance_data = balance_response.json()
        
        assert balance_data["total_income"] == 5000.00
        assert balance_data["total_expenses"] == 1500.00
        assert balance_data["current_balance"] == 3500.00

    def test_balance_updates_on_transaction_update(self, test_user, test_category, auth_headers):
        """Testa se balance é recalculado ao atualizar transação."""
        # Cria transação
        create_response = client.post("/transactions/", json={
            "user_id": test_user["id"],
            "description": "Shopping",
            "amount": 100.00,
            "transaction_type": "expense",
            "category_id": test_category["id"]
        }, headers=auth_headers)
        transaction_id = create_response.json()["id"]
        
        # Atualiza valor
        client.put(f"/transactions/{transaction_id}", json={"amount": 150.00}, headers=auth_headers)
        
        # Verifica balance
        balance_response = client.get(f"/balances/{test_user['id']}", headers=auth_headers)
        balance_data = balance_response.json()
        assert balance_data["total_expenses"] == 150.00

    def test_balance_updates_on_transaction_deletion(self, test_user, test_category, auth_headers):
        """Testa se balance é recalculado ao deletar transação."""
        # Cria transação
        create_response = client.post("/transactions/", json={
            "user_id": test_user["id"],
            "description": "Test",
            "amount": 200.00,
            "transaction_type": "expense",
            "category_id": test_category["id"]
        }, headers=auth_headers)
        transaction_id = create_response.json()["id"]
        
        # Deleta transação
        client.delete(f"/transactions/{transaction_id}", headers=auth_headers)
        
        # Verifica balance
        balance_response = client.get(f"/balances/{test_user['id']}", headers=auth_headers)
        balance_data = balance_response.json()
        assert balance_data["total_expenses"] == 0.0
        assert balance_data["current_balance"] == 0.0
