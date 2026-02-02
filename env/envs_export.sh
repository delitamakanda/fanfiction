#!/bin/bash
# Environment variables export script
# This script exports all necessary environment variables for the application
# It can be sourced on the VM to set up the environment

# Django settings
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-backend.settings_production}"

# Security
if [ -n "${SECRET_KEY:-}" ]; then
    export SECRET_KEY="$SECRET_KEY"
fi

# Database configuration
if [ -n "${ALIYUN_BDD_NAME:-}" ]; then
    export ALIYUN_BDD_NAME="$ALIYUN_BDD_NAME"
fi
if [ -n "${ALIYUN_BDD_USER:-}" ]; then
    export ALIYUN_BDD_USER="$ALIYUN_BDD_USER"
fi
if [ -n "${ALIYUN_BDD_PASSWORD:-}" ]; then
    export ALIYUN_BDD_PASSWORD="$ALIYUN_BDD_PASSWORD"
fi
if [ -n "${ALIYUN_BDD_HOST:-}" ]; then
    export ALIYUN_BDD_HOST="$ALIYUN_BDD_HOST"
fi
if [ -n "${ALIYUN_BDD_PORT:-}" ]; then
    export ALIYUN_BDD_PORT="$ALIYUN_BDD_PORT"
fi

# ReCAPTCHA configuration
if [ -n "${RECAPTCHA_SECRET_KEY:-}" ]; then
    export RECAPTCHA_SECRET_KEY="$RECAPTCHA_SECRET_KEY"
fi

# Debug mode
export DEBUG="${DEBUG:-False}"

# Admin configuration
if [ -n "${ADMIN_EMAIL:-}" ]; then
    export ADMIN_EMAIL="$ADMIN_EMAIL"
fi
if [ -n "${ADMIN_NAME:-}" ]; then
    export ADMIN_NAME="$ADMIN_NAME"
fi

# SendGrid email configuration
if [ -n "${SENDGRID_SERVER:-}" ]; then
    export SENDGRID_SERVER="$SENDGRID_SERVER"
fi
if [ -n "${SENDGRID_PORT:-}" ]; then
    export SENDGRID_PORT="$SENDGRID_PORT"
fi
if [ -n "${SENDGRID_USERNAME:-}" ]; then
    export SENDGRID_USERNAME="$SENDGRID_USERNAME"
fi
if [ -n "${SENDGRID_PASSWORD:-}" ]; then
    export SENDGRID_PASSWORD="$SENDGRID_PASSWORD"
fi

# Aliyun OSS configuration
if [ -n "${OSS_ACCESS_KEY_ID:-}" ]; then
    export OSS_ACCESS_KEY_ID="$OSS_ACCESS_KEY_ID"
fi
if [ -n "${OSS_ACCESS_KEY_SECRET:-}" ]; then
    export OSS_ACCESS_KEY_SECRET="$OSS_ACCESS_KEY_SECRET"
fi
if [ -n "${OSS_EXPIRE_TIME:-}" ]; then
    export OSS_EXPIRE_TIME="$OSS_EXPIRE_TIME"
fi
if [ -n "${OSS_BUCKET_NAME:-}" ]; then
    export OSS_BUCKET_NAME="$OSS_BUCKET_NAME"
fi
if [ -n "${OSS_ENDPOINT:-}" ]; then
    export OSS_ENDPOINT="$OSS_ENDPOINT"
fi

# Python environment
export PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
export PYTHONUNBUFFERED="${PYTHONUNBUFFERED:-1}"

echo "Environment variables exported successfully"
