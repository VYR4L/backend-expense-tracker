# 💸 Expense Tracker API - Backend

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-14354C?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.121.2-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

<p align="center">
  API para gerenciamento de despesas pessoais, desenvolvida com Python, FastAPI, SQLAlchemy e MySQL.
</p>

---

## 🎯 Sobre o Projeto

Este projeto é o backend de um sistema de controle de despesas, com autenticação JWT, rotas protegidas, integração com MySQL e arquitetura escalável para produção. Este backend gerencia usuários, categorias, transações, metas e saldos, garantindo isolamento por usuário e autenticação JWT.


### 🔧 Principais Tecnologias

![Python](https://img.shields.io/badge/python-14354C?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-4E8DBE?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)


## ✨ Características

- 🔒 Autenticação JWT
- 🧑‍💼 Rotas protegidas para admin
- 📊 CRUD completo para usuários, transações, categorias, metas e saldos
- 🛡️ Permissões customizadas
- 🐳 Deploy com Docker e Docker Compose
- 🧪 Testes automatizados com Pytest

## 🚀 Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **FastAPI 0.110** - Framework web
- **SQLAlchemy 2.0** - ORM
- **MySQL 8.0** - Banco de dados relacional
- **Docker 24.0** - Containerização
- **Pytest** - Testes automatizados


## 📁 Estrutura do Projeto

```
backend-expense-tracker/
├── api/
│   └── routes/         # Rotas da API (auth, transactions, categories, etc)
├── auth/               # Autenticação e login
├── controllers/        # Lógica dos endpoints
├── models/             # Modelos ORM
├── services/           # Regras de negócio
├── tests/              # Testes automatizados
├── utils/              # Utilitários
├── config.py           # Configuração da aplicação
├── main.py             # Ponto de entrada FastAPI
├── requirements.txt    # Dependências Python
├── Dockerfile          # Build da imagem Docker
├── docker-compose.yml  # Orquestração dos containers
├── .env.example        # Exemplo de variáveis de ambiente
└── README.md           # Documentação
```

## ⚙️ Configuração do Ambiente

### 1. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e preencha os valores:

```sh
cp .env.example .env
```

- Gere valores seguros para JWT e tokens usando o script:

```sh
bash generate-secrets.sh
```

- Cole os valores gerados no seu `.env`.

### 2. Instalação Local

Instale as dependências:

```sh
pip install -r requirements.txt
```

### 3. Execução Local

Inicie o banco de dados MySQL (recomendado via Docker Compose):

```sh
docker-compose up mysql
```

Execute a API:

```sh
uvicorn main:app --reload
```

### 4. Execução com Docker Compose

Para rodar toda a stack (API + MySQL):

```sh
docker-compose up --build
```

Acesse a API em [http://localhost:8000](http://localhost:8000)

## 🐳 Docker

- O projeto já possui `Dockerfile` e `docker-compose.yml` configurados para produção.
- As variáveis de ambiente são lidas do arquivo `.env`.
- O serviço MySQL é inicializado com persistência de dados.

## 🧪 Testes

- Testes automatizados em `tests/`
- Para rodar: `pytest`
- Testes garantem isolamento por usuário, validação de campos e resposta paginada


---

<p align="center">
  Desenvolvido com 💜 por Felipe Kravec Zanatta
</p>
