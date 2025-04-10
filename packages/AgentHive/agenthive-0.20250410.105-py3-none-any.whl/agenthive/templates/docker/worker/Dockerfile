FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl wget vim tree procps \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir agenthive

COPY src/ ./src/

RUN if [ -d "/app/src/workers/requirements" ]; then \
    for req in /app/src/workers/requirements/*.txt; do \
        [ -f "$req" ] && pip install --no-cache-dir -r "$req" || true; \
    done; \
fi

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import agenthive.utils.health; agenthive.utils.health.check_worker_health()" || exit 1

# Run worker
CMD ["python", "-m", "agenthive.service.worker.main", "--scan-dir", "/app/src/workers"]
