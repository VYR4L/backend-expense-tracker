#!/bin/bash

# Script de geração de senhas seguras para produção
# Execute este script e copie os valores para seu .env.prod

echo "==================================================="
echo "  GERADOR DE SENHAS PARA PRODUÇÃO"
echo "==================================================="
echo ""

echo "JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")"
echo ""

echo "ADMIN_TOKEN=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")"
echo ""

echo "DB_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")"
echo ""

echo "MYSQL_ROOT_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")"
echo ""

echo "==================================================="
echo "  COPIE OS VALORES ACIMA PARA SEU .env.prod"
echo "==================================================="
