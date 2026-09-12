# PyAuthService - Django OAuth2/JWT Authentication Service
# Keep build-only tooling and pip metadata out of the runtime image.
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# psycopg2-binary normally uses a wheel, but retaining the compiler in this
# stage keeps builds portable without adding it to the final image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --no-compile --prefix=/install -r requirements.txt

# Final stage: no compiler, PostgreSQL CLI, or pip cache.
FROM python:3.11-slim-bookworm

WORKDIR /app

# netcat is used by entrypoint.sh to wait for PostgreSQL.
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy only the installed runtime packages and console scripts.
COPY --from=builder /install /usr/local

# Create the same UID used by docker-compose and copy files with ownership set
# during the image build to avoid a recursive chown layer.
RUN useradd --create-home --uid 1000 appuser

COPY --chown=appuser:appuser . .

RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV PATH=/usr/local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

USER appuser

# Expose port
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import http.client; conn = http.client.HTTPConnection('localhost', int('${PORT}')); conn.request('GET', '/health/'); exit(0 if conn.getresponse().status == 200 else 1)" || exit 1

# Run application with gunicorn (production-ready)
CMD ["gunicorn", "pyauthservice.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
