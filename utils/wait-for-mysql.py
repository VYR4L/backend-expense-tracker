#!/usr/bin/env python3
"""Script para aguardar o MySQL estar pronto antes de iniciar o FastAPI."""
import time
import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent

sys.path.append(str(root_dir))
from config import settings

import pymysql


def wait_for_mysql(max_retries=30, delay=2):
    """Tenta conectar ao MySQL até conseguir ou esgotar tentativas."""
    print(f"🔍 Aguardando MySQL em {settings.DB_HOST}:{settings.DB_PORT}...")
    
    for attempt in range(1, max_retries + 1):
        try:
            connection = pymysql.connect(
                host=settings.DB_HOST,
                port=int(settings.DB_PORT),
                user=settings.DB_USERNAME,
                password=settings.DB_PASSWORD,
                database=settings.DB_DATABASE,
                connect_timeout=5
            )
            connection.close()
            print(f"✅ MySQL pronto após {attempt} tentativa(s)!")
            return True
        except pymysql.err.OperationalError as e:
            print(f"⏳ Tentativa {attempt}/{max_retries}: MySQL não disponível ainda... ({e})")
            if attempt < max_retries:
                time.sleep(delay)
            else:
                print("❌ MySQL não ficou disponível no tempo esperado.")
                return False
    
    return False


if __name__ == "__main__":
    if not wait_for_mysql():
        sys.exit(1)
    print("🚀 Iniciando aplicação...")
