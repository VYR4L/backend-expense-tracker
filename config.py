from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()


class Settings:
    """Configurações da aplicação."""
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database - aceita DATABASE_URL do DigitalOcean ou variáveis individuais
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_DATABASE: str = os.getenv("DB_DATABASE", "expense_tracker")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    @classmethod
    def get_database_url(cls) -> str:
        """Retorna a URL de conexão do banco de dados."""
        # Se DATABASE_URL estiver configurada (DigitalOcean), use ela
        if cls.DATABASE_URL:
            # Substitui mysql:// por mysql+pymysql:// para o driver correto
            url = cls.DATABASE_URL.replace("mysql://", "mysql+pymysql://")
            
            # Remove ssl-mode (não suportado pelo PyMySQL) e adiciona parâmetros SSL corretos
            if "ssl-mode=REQUIRED" in url or "ssl-mode=required" in url:
                url = url.replace("ssl-mode=REQUIRED", "ssl_disabled=false")
                url = url.replace("ssl-mode=required", "ssl_disabled=false")
            elif "ssl-mode=" in url:
                # Remove qualquer outro valor de ssl-mode
                import re
                url = re.sub(r'[?&]ssl-mode=[^&]*', '', url)
                # Adiciona parâmetro SSL correto
                url += "&ssl_disabled=false" if "?" in url else "?ssl_disabled=false"
            
            return url
        
        # Caso contrário, constrói a URL a partir das variáveis individuais
        from urllib.parse import quote_plus
        password_encoded = quote_plus(cls.DB_PASSWORD)
        return f"mysql+pymysql://{cls.DB_USERNAME}:{password_encoded}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_DATABASE}"

    ALLOWED_ORIGINS: List[str] = os.getenv('ALLOWED_ORIGINS', '*').split(',')

    LOG_LEVEL: str = 'debug' if DEBUG else 'info'
    
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    @classmethod
    def validate(cls) -> None:
        """Valida as configurações essenciais."""
        # Future JWT validation example:
        # if not cls.JWT_SECRET:
        #     raise ValueError("JWT_SECRET must be set in environment variables")
        
        if "*" in cls.ALLOWED_ORIGINS and not cls.DEBUG:
            raise ValueError("ALLOWED_ORIGINS cannot be '*' in production mode")

    @classmethod
    def get_info(cls) -> dict:
        """Retorna informações sobre as configurações"""
        return {
            "host": cls.APP_HOST,
            "port": cls.APP_PORT,
            "debug": cls.DEBUG,
            "jwt_algorithm": cls.JWT_ALGORITHM,
            "allowed_origins": cls.ALLOWED_ORIGINS,
            "log_level": cls.LOG_LEVEL,
        }

settings = Settings()

# Base precisa ser criada antes de importar os models
Base = declarative_base()

# Engine e SessionLocal podem ser None inicialmente (para testes)
engine = None
SessionLocal = None

def init_db():
    """Inicializa a conexão com o banco de dados."""
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(
            settings.get_database_url(),
            pool_pre_ping=True,
            echo=settings.DEBUG
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine

def get_db():
    """Dependency para obter sessão do banco."""
    if SessionLocal is None:
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

