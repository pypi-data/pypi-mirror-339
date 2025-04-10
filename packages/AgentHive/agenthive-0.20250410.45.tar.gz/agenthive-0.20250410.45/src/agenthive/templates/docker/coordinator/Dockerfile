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
    curl vim tree wget procps \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir agenthive

COPY src/ ./src/

RUN mkdir -p /etc/supervisor/conf.d
COPY docker/coordinator/config/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/coordinator/config/app-coordinator.conf /etc/supervisor/conf.d/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose ports
EXPOSE 8000

# Run coordinator
#CMD ["python", "-m", "agenthive.service.coordinator.main"]
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
