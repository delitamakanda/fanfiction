#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Check if we're in production environment (via SSH or deployment)
    # If DJANGO_SETTINGS_MODULE is already set, respect it
    # Otherwise, default to backend.settings (development)
    if "DJANGO_SETTINGS_MODULE" not in os.environ:
        # Check for production environment indicators
        # If any production database environment variables are set, use production settings
        production_vars = [
            'ALIYUN_BDD_NAME',
            'ALIYUN_BDD_HOST',
            'ALIYUN_BDD_USER',
        ]
        
        # If any production database variables exist, assume production environment
        if any(os.environ.get(var) for var in production_vars):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings_production")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
