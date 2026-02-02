# Deployment Guide

## Running Migrations on Production (Aliyun/Apsara Database)

### Via SSH

When you SSH into the production server, the `manage.py` script will automatically detect the production environment and use the correct database configuration.

#### Prerequisites

Make sure the following environment variables are set on your production server:
- `ALIYUN_BDD_NAME` - Database name
- `ALIYUN_BDD_HOST` - Database host
- `ALIYUN_BDD_USER` - Database user
- `ALIYUN_BDD_PASSWORD` - Database password
- `ALIYUN_BDD_PORT` - Database port (optional, defaults to PostgreSQL standard)

#### Running Migrations

Simply run the standard Django migration command:

```bash
python manage.py migrate
```

The script will automatically:
1. Detect that production environment variables are set
2. Use `backend.settings_production` instead of `backend.settings`
3. Connect to the Apsara PostgreSQL database

#### Manual Settings Override

If you need to explicitly specify which settings to use:

```bash
# Use production settings
DJANGO_SETTINGS_MODULE=backend.settings_production python manage.py migrate

# Use development settings (even in production environment)
DJANGO_SETTINGS_MODULE=backend.settings python manage.py migrate
```

#### Other Useful Commands

```bash
# Check migration status
python manage.py showmigrations

# Create new migrations
python manage.py makemigrations

# Apply specific migration
python manage.py migrate app_name migration_name

# Rollback migration
python manage.py migrate app_name previous_migration_name
```

### Via Docker/Entrypoint

When deploying via Docker, migrations are automatically run by the `entrypoint.sh` script, which always uses production settings:

```bash
# In entrypoint.sh
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-backend.settings_production}"
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

## Troubleshooting

### Migrations Running on Wrong Database

If migrations are running on SQLite instead of PostgreSQL:

1. Check that production environment variables are set:
   ```bash
   echo $ALIYUN_BDD_NAME
   echo $ALIYUN_BDD_HOST
   ```

2. If they're not set, export them:
   ```bash
   export ALIYUN_BDD_NAME=your_database_name
   export ALIYUN_BDD_HOST=your_database_host
   export ALIYUN_BDD_USER=your_database_user
   export ALIYUN_BDD_PASSWORD=your_database_password
   ```

3. Then run migrations again:
   ```bash
   python manage.py migrate
   ```

### Database Connection Issues

If you encounter connection errors:

1. Verify database credentials are correct
2. Check that the database server is accessible from your SSH session
3. Verify firewall rules allow connections to the database port
4. Check the database connection timeout settings in `backend/settings_production.py`

### Testing Database Connection

To test if Django can connect to the database:

```bash
python manage.py dbshell
```

This will open a PostgreSQL shell if the connection is successful.
