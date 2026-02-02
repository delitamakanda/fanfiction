# GitHub Secrets Configuration Guide

## Overview
This document explains how to configure secrets for GitHub Actions workflows in this repository.

## Repository Secrets vs Environment Secrets

### Repository Secrets
- **Scope**: Available to all workflows in the repository
- **Location**: Settings > Secrets and variables > Actions > Repository secrets
- **Use case**: General secrets needed across all workflows
- **Access control**: Anyone with write access to the repository can use these secrets
- **This is what we use in this project**

### Environment Secrets
- **Scope**: Only available to workflows that specify a particular environment
- **Location**: Settings > Environments > [environment-name] > Environment secrets
- **Use case**: Production secrets that need additional protection
- **Access control**: Can require reviewers, restrict to specific branches, add wait timers
- **We do NOT use this approach** to keep configuration simpler

## Why We Use Repository Secrets

Previously, the `deploy-docker.yml` workflow used `environment: fanfiction-fr`, which required secrets to be configured as Environment secrets. This created confusion because:

1. The CI workflow (`django.yml`) used Repository secrets
2. The deploy workflow used Environment secrets
3. Users had to configure secrets in two different places

**We have now standardized on Repository secrets** for simplicity and consistency.

## Required Secrets

All the following secrets must be configured at:
**Settings > Secrets and variables > Actions > Repository secrets**

### Core Django Secrets
- `SECRET_KEY` - Django secret key for cryptographic signing
- `DEBUG` - Debug mode setting (should be "False" for production)
- `DJANGO_SETTINGS_MODULE` - Django settings module to use

### Database Configuration
- `ALIYUN_BDD_NAME` - Database name
- `ALIYUN_BDD_USER` - Database user
- `ALIYUN_BDD_PASSWORD` - Database password
- `ALIYUN_BDD_HOST` - Database host
- `ALIYUN_BDD_PORT` - Database port

### Email Configuration (SendGrid)
- `ADMIN_EMAIL` - Administrator email address
- `ADMIN_NAME` - Administrator name
- `SENDGRID_SERVER` - SendGrid SMTP server
- `SENDGRID_PORT` - SendGrid SMTP port
- `SENDGRID_USERNAME` - SendGrid username
- `SENDGRID_PASSWORD` - SendGrid password

### Storage Configuration (Aliyun OSS)
- `OSS_ACCESS_KEY_ID` - Aliyun OSS access key ID
- `OSS_ACCESS_KEY_SECRET` - Aliyun OSS access key secret
- `OSS_EXPIRE_TIME` - OSS URL expiration time
- `OSS_BUCKET_NAME` - OSS bucket name
- `OSS_ENDPOINT` - OSS endpoint URL

### Other Services
- `RECAPTCHA_SECRET_KEY` - Google reCAPTCHA secret key
- `REDIS_URL` - Redis connection URL (for CI/testing)

### Deployment Secrets
- `DOCKER_PASSWORD` - Docker Hub password
- `ECS_HOST` - Alibaba ECS server hostname/IP
- `ECS_USERNAME` - SSH username for ECS
- `ECS_SSH_KEY` - Private SSH key for ECS authentication
- `ECS_SSH_PORT` - SSH port for ECS (usually 22)

## Required Variables

Configuration variables (non-secret) must be set at:
**Settings > Secrets and variables > Actions > Variables > Repository variables**

- `DOCKER_USERNAME` - Docker Hub username

## How to Configure Secrets

1. Go to your repository on GitHub
2. Click on **Settings**
3. In the left sidebar, expand **Secrets and variables**
4. Click on **Actions**
5. Under **Repository secrets**, click **New repository secret**
6. Add each secret with its name and value
7. Click **Add secret**

## Verifying Configuration

After configuring all secrets:

1. Check the workflow runs in the **Actions** tab
2. If secrets are missing, the workflow will fail with an error indicating which secret is not found
3. The deploy workflow will log environment variables (without exposing values) to help verify configuration

## Migration from Environment Secrets

If you previously configured secrets as Environment secrets:

1. Go to **Settings > Environments > fanfiction-fr**
2. Copy all secret values (you may need to recreate them as GitHub doesn't show values)
3. Add them as Repository secrets following the steps above
4. You can delete the Environment secrets once migration is complete
5. The `fanfiction-fr` environment can be deleted if no longer needed

## Security Best Practices

- Never commit secrets to the repository
- Rotate secrets regularly, especially after team member changes
- Use strong, randomly generated values for `SECRET_KEY` and other sensitive credentials
- Keep `DEBUG=False` in production
- Limit repository access to trusted team members only
- Review workflow logs carefully - avoid printing secret values

## Troubleshooting

### Workflow fails with "secret not found"
- Verify the secret is configured at the Repository level (not Environment level)
- Check the secret name matches exactly (case-sensitive)
- Ensure you have saved the secret (not just previewed it)

### Deployment fails with authentication errors
- Verify ECS SSH key is properly formatted (includes BEGIN/END markers)
- Check DOCKER_PASSWORD is correct
- Verify database credentials are correct

### Application errors after deployment
- Check that all application secrets are set correctly
- Review Docker container logs: `docker logs fanfiction`
- Verify environment variables in container: `docker exec fanfiction env`

## Additional Resources

- [GitHub Actions: Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Using environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
