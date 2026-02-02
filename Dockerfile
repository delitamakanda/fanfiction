FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    postgresql-client \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file to the container and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Create /env directory and copy environment export script
RUN mkdir -p /env
COPY env/envs_export.sh /env/envs_export.sh
RUN chmod +x /env/envs_export.sh


# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose the port the container will run on
EXPOSE 8000

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health/', timeout=2)" || exit 1

# Set entrypoint to run migrations before starting the application
ENTRYPOINT ["/entrypoint.sh"]

# Run the application with optimized Gunicorn settings
CMD ["gunicorn", "backend.wsgi:application", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "3", \
    "--threads", "4", \
    "--timeout", "120", \
    "--graceful-timeout", "30", \
    "--worker-class", "gthread", \
    "--access-logfile", "-", \
    "--error-logfile", "-", \
    "--log-level", "info"]
