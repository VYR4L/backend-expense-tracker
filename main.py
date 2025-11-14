from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import user_routes
import uvicorn
from config import settings, Base
from models import users
import os


try:
    settings.validate()
except Exception as e:
    print(f"Erro nas configurações da aplicação: {str(e)}")
    exit(1)

# Inicializa e cria as tabelas no banco apenas se não for teste
if os.getenv("TESTING") != "true":
    from config import init_db
    engine = init_db()
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="API para gerenciamento de despesas pessoais.",
    version="1.0.0",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)

@app.get("/")
async def root():
    return {
        "service": "Expense Tracker API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/config")
async def get_config():
    return settings.get_info()

if __name__ == "__main__":
    print("Starting Expense Tracker API...")
    print(f"Host: {settings.APP_HOST}, Port: {settings.APP_PORT}, Debug: {settings.DEBUG}")

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL
    )