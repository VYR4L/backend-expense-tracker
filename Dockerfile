# -----------------------------
# 1) Imagem base leve
# -----------------------------
FROM python:3.11-slim AS base

# Evita buffers no log
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# -----------------------------
# 2) Instala dependências Python
# -----------------------------
WORKDIR /app

# Copia o requirements para aproveitar cache
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# -----------------------------
# 3) Copia código da aplicação
# -----------------------------
COPY . .

# Expor a porta do FastAPI
EXPOSE 8000

# -----------------------------
# 4) Comando para iniciar o serviço
# -----------------------------
CMD ["sh", "-c", "python utils/wait-for-mysql.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
