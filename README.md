<h1 align="center">💸 Expense Tracker Backend - Felipe Kravec Zanatta</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-14354C?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-4E8DBE?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

<p align="center">
  API backend para controle de despesas, desenvolvido com FastAPI, SQLAlchemy e MySQL. <br/>
  <b>Esta branch é dedicada ao deploy no Digital Ocean.</b>
</p>

---

## 🎯 Sobre o Projeto

Este backend gerencia usuários, categorias, transações, metas e saldos, garantindo isolamento por usuário e autenticação JWT. A branch <b>deploy/digital-ocean</b> contém configurações específicas para deploy na nuvem Digital Ocean, incluindo Docker e variáveis de ambiente.

## 👨‍💻 Sobre Mim

🎓 Estudante de Ciência da Computação na UNIOESTE  
💻 Desenvolvedor Fullstack com foco em Backend  
🚀 Apaixonado por tecnologia e sempre em busca de novos aprendizados  

### 🔧 Principais Tecnologias

![Python](https://img.shields.io/badge/python-14354C?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-4E8DBE?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

## ✨ Características

- 🔒 Isolamento de dados por usuário (JWT)
- 📅 Transações com campo de data customizável
- 📊 Resposta paginada com metadados (total, page, limit)
- 🧩 Arquitetura modular: models, services, controllers, routes
- 🐳 Deploy automatizado via Docker Compose
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
│   └── routes/           # Rotas da API (auth, transactions, categories, etc)
├── auth/                 # Autenticação e serviços de login
├── controllers/          # Lógica de controle das rotas
├── models/               # Modelos ORM e schemas Pydantic
├── services/             # Regras de negócio
├── tests/                # Testes automatizados
├── utils/                # Utilitários
├── config.py             # Configurações globais
├── docker-compose.yml    # Orquestração Docker
├── Dockerfile            # Build da imagem
├── requirements.txt      # Dependências Python
├── main.py               # Entry point FastAPI
└── README.md             # Documentação
```

## 🛠️ Deploy no Digital Ocean

Esta branch (<b>deploy/digital-ocean</b>) inclui configurações específicas para deploy na Digital Ocean:
- Dockerfile e docker-compose otimizados para produção
- Scripts para geração de segredos e variáveis de ambiente
- Persistência de dados via volumes Docker
- Recomenda-se configurar variáveis sensíveis via painel da Digital Ocean

## 🔑 Autenticação

- JWT para autenticação e isolamento de dados
- Usuário não envia user_id nas requisições; backend identifica pelo token
- Todas as operações de transações e categorias são isoladas por usuário

## 📦 Endpoints Principais

- `/auth/login` - Autenticação e geração de token JWT
- `/transactions` - CRUD de transações (com paginação e filtro por data)
- `/categories` - CRUD de categorias
- `/goals` - CRUD de metas
- `/balances` - Consulta de saldo

## 🧪 Testes

- Testes automatizados em `tests/`
- Para rodar: `pytest`
- Testes garantem isolamento por usuário, validação de campos e resposta paginada

---

<p align="center">
  Desenvolvido com 💜 por Felipe Kravec Zanatta
</p>
