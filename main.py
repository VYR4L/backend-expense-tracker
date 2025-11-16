from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.routes import user_routes, balance_routes, categories_routes, goals_routes, transactions_routes, auth_routes
import uvicorn
from config import settings, Base
from utils.permissions import verify_admin_token
import os


try:
    settings.validate()
except Exception as e:
    print(f"Erro nas configurações da aplicação: {str(e)}")
    exit(1)

app = FastAPI(
    title="Expense Tracker API",
    description="API para gerenciamento de despesas pessoais.",
    version="1.0.0",
    debug=settings.DEBUG,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json",
    dependencies=[Depends(verify_admin_token)] if not settings.DEBUG else [],
)

@app.on_event("startup")
async def startup_event():
    """Inicializa o banco de dados na inicialização da aplicação."""
    if os.getenv("TESTING") != "true":
        try:
            from config import init_db
            engine = init_db()
            Base.metadata.create_all(bind=engine, checkfirst=True)
            print("✅ Tabelas do banco de dados criadas/verificadas com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco de dados: {str(e)}")
            print(f"⚠️ Verifique as configurações de conexão: DB_HOST={settings.DB_HOST}, DB_DATABASE={settings.DB_DATABASE}")
            # Não mata a aplicação - deixa rodar para poder ver os logs

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(balance_routes.router)
app.include_router(categories_routes.router)
app.include_router(goals_routes.router)
app.include_router(transactions_routes.router)

@app.get("/")
async def root():
    return {
        "service": "Expense Tracker API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check(admin: bool = Depends(verify_admin_token)):
    return {"status": "healthy"}

@app.get("/config")
async def get_config(admin: bool = Depends(verify_admin_token)):
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