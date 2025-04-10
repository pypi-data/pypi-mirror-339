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
    curl \
    nodejs \
    npm \
    vim tree wget procps \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir agenthive

COPY src/ ./src/

RUN mkdir -p /etc/supervisor/conf.d
COPY docker/monitor/config/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/monitor/config/app-monitor.conf /etc/supervisor/conf.d/

# Build frontend
WORKDIR /app/src/monitor/frontend
RUN bash -c 'test -r package.json && npm install && npm run build || echo "No frontend build required"'
# Keep the frontend build in the backend directory
RUN mkdir -p /app/src/agenthive/service/monitor/frontend/dist/static
RUN touch /app/src/agenthive/service/monitor/frontend/dist/static/index.html

# Return to app directory
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose ports
EXPOSE 8080

# Run monitor
#CMD ["python", "-m", "agenthive.service.monitor.backend.main"]
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
