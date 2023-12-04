#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from utils.general import get_settings_path
from core.utils.dotenv import load_env, get_env_value
from core import BASE_DIR


env_path = os.path.join(BASE_DIR, ".env")
load_env(env_path)


def main():
    """Run administrative tasks."""
    production_env = bool(int(get_env_value("PROD")))
    settings_path = get_settings_path(prod=production_env)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_path)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
