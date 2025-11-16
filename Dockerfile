# -----------------------------
# Stage 1: Build
# -----------------------------
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user --no-warn-script-location -r requirements.txt

# -----------------------------
# Stage 2: Runtime
# -----------------------------
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

WORKDIR /app

# Instala apenas runtime necessário
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root antes de copiar as dependências
RUN useradd -m -u 1000 appuser

# Copia dependências instaladas do stage builder para o diretório do appuser
COPY --from=builder /root/.local /home/appuser/.local

# Copia código da aplicação
COPY . .

# Ajusta permissões
RUN chown -R appuser:appuser /app /home/appuser/.local

USER appuser

# Expor a porta do FastAPI
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Comando para iniciar o serviço
CMD ["sh", "-c", "python utils/wait-for-mysql.py && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --proxy-headers --forwarded-allow-ips='*'"]
