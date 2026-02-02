# Environment Variables Export

This directory contains the `envs_export.sh` script for exporting environment variables on the VM or within the Docker container.

## Usage

### On the VM

To set up environment variables on the VM, you can source the script:

```bash
source /env/envs_export.sh
```

This will export all the necessary environment variables for the application.

### With BUILD_COMMAND

If you need to run a build command after setting up the environment, you can set the `BUILD_COMMAND` environment variable before sourcing the script or before starting the container:

```bash
# Set the BUILD_COMMAND
export BUILD_COMMAND="python manage.py migrate && python manage.py collectstatic --noinput"

# Source the environment variables
source /env/envs_export.sh

# The BUILD_COMMAND will be executed automatically by entrypoint.sh
```

### Docker Container

When running the Docker container, you can pass the `BUILD_COMMAND` as an environment variable:

```bash
docker run -d --name fanfiction \
  -p 8000:8000 \
  --env-file /tmp/fanfiction.env \
  -e BUILD_COMMAND="python manage.py custom_command" \
  --restart unless-stopped \
  fanfiction:latest
```

The entrypoint script will automatically:
1. Source `/env/envs_export.sh` if it exists
2. Execute the `BUILD_COMMAND` if it's set
3. Run migrations and collect static files
4. Start the application

## Environment Variables

The `envs_export.sh` script exports the following environment variables:

- `DJANGO_SETTINGS_MODULE` - Django settings module (default: backend.settings_production)
- `SECRET_KEY` - Django secret key
- `ALIYUN_BDD_*` - Aliyun database configuration
- `RECAPTCHA_SECRET_KEY` - ReCAPTCHA secret key
- `DEBUG` - Debug mode (default: False)
- `ADMIN_EMAIL`, `ADMIN_NAME` - Admin configuration
- `SENDGRID_*` - SendGrid email configuration
- `OSS_*` - Aliyun OSS storage configuration
- `PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED` - Python environment variables

All variables use default values if not already set, allowing for flexible configuration.

## Manual Operations on VM

For manual operations on the VM (like running management commands), you can:

1. SSH into the VM
2. Source the environment variables:
   ```bash
   source /env/envs_export.sh
   ```
3. Execute your commands:
   ```bash
   docker exec fanfiction python manage.py your_command
   ```

Or directly inside the container:
```bash
docker exec -it fanfiction bash
source /env/envs_export.sh
python manage.py your_command
```
