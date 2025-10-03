# Multi-stage build for Railway deployment
FROM python:3.11-slim as backend-builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy application code
COPY backend /app/backend
COPY storage /app/storage

# Set working directory to backend
WORKDIR /app/backend

# Declare Railway build arguments (Railway automatically passes all variables as build args)
ARG DATABASE_URL
ARG REDIS_URL
ARG SECRET_KEY
ARG OPENAI_API_KEY
ARG ANTHROPIC_API_KEY
ARG AI_PROVIDER
ARG DEBUG
ARG LOG_LEVEL
ARG ENVIRONMENT

# Convert build args to runtime environment variables
ENV DATABASE_URL=$DATABASE_URL
ENV REDIS_URL=$REDIS_URL
ENV SECRET_KEY=$SECRET_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
ENV AI_PROVIDER=${AI_PROVIDER:-openai}
ENV DEBUG=${DEBUG:-false}
ENV LOG_LEVEL=${LOG_LEVEL:-INFO}
ENV ENVIRONMENT=${ENVIRONMENT:-production}

# Set application environment
ENV PYTHONPATH=/app/backend
ENV PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/api/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
