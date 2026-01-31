FROM python:3.12-slim

ARG SECRET_KEY
ARG DEBUG
ARG ADMIN_EMAIL
ARG ADMIN_NAME
ARG SENDGRID_SERVER
ARG SENDGRID_PORT
ARG SENDGRID_USERNAME
ARG SENDGRID_PASSWORD
ARG OSS_ACCESS_KEY_ID
ARG OSS_ACCESS_KEY_SECRET
ARG OSS_EXPIRE_TIME=3600
ARG OSS_BUCKET_NAME
ARG OSS_ENDPOINT
ARG ALIYUN_BDD_NAME
ARG ALIYUN_BDD_USER
ARG ALIYUN_BDD_PASSWORD
ARG ALIYUN_BDD_HOST
ARG ALIYUN_BDD_PORT
ARG DJANGO_SETTINGS_MODULE=backend.settings_production
ARG RECAPTCHA_SECRET_KEY

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=${SECRET_KEY:-'dummus_key_for_production_environment'}
ENV DEBUG=${DEBUG}
ENV ADMIN_EMAIL=${ADMIN_EMAIL}
ENV ADMIN_NAME=${ADMIN_NAME}
ENV SENDGRID_SERVER=${SENDGRID_SERVER}
ENV SENDGRID_PORT=${SENDGRID_PORT}
ENV SENDGRID_USERNAME=${SENDGRID_USERNAME}
ENV SENDGRID_PASSWORD=${SENDGRID_PASSWORD}
ENV OSS_ACCESS_KEY_ID=${OSS_ACCESS_KEY_ID}
ENV OSS_ACCESS_KEY_SECRET=${OSS_ACCESS_KEY_SECRET}
ENV OSS_EXPIRE_TIME=${OSS_EXPIRE_TIME:-3600}
ENV OSS_BUCKET_NAME=${OSS_BUCKET_NAME}
ENV OSS_ENDPOINT=${OSS_ENDPOINT}
ENV ALIYUN_BDD_NAME=${ALIYUN_BDD_NAME}
ENV ALIYUN_BDD_USER=${ALIYUN_BDD_USER}
ENV ALIYUN_BDD_PASSWORD=${ALIYUN_BDD_PASSWORD}
ENV ALIYUN_BDD_HOST=${ALIYUN_BDD_HOST}
ENV ALIYUN_BDD_PORT=${ALIYUN_BDD_PORT}
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
ENV RECAPTCHA_SECRET_KEY=${RECAPTCHA_SECRET_KEY}

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


# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose the port the container will run on
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health/', timeout=2)" || exit 1

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
