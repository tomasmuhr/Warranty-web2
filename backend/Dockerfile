# ==========================================
# STAGE 1: development (Used in development)
# ==========================================
FROM python:3.14-alpine AS development

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

# Development command with hot-reload enabled
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ==========================================
# STAGE 2: production (Used in production)
# ==========================================
FROM python:3.14-alpine AS production

WORKDIR /app

# Copy installed dependencies from the developer stage to keep this layer clean
# COPY --from=development /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
# COPY --from=development /usr/local/bin /usr/local/bin

# Replaces copy of installed dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

# Production command (no reload, optimized)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]