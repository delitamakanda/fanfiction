#!/bin/bash
set -euo pipefail

# Source environment variables if the export script exists
if [ -f /env/envs_export.sh ]; then
    echo "Sourcing environment variables from /env/envs_export.sh"
    source /env/envs_export.sh
else
    # Fallback to default DJANGO_SETTINGS_MODULE
    export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-backend.settings_production}"
fi

# Execute optional build command if BUILD_COMMAND is set
# Note: BUILD_COMMAND should only be set by trusted deployment scripts or administrators
# as it allows arbitrary command execution. Do not expose this to user input.
if [ -n "${BUILD_COMMAND:-}" ]; then
    echo "Executing BUILD_COMMAND: $BUILD_COMMAND"
    eval "$BUILD_COMMAND"
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
