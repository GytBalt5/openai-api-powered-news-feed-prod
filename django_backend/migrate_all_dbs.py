#!/usr/bin/env python
import os

from utils.general import get_settings_path
from core.utils.dotenv import load_env, get_env_value
from core.utils.database_config import (
    AUTH_DB_ALIAS,
    NEWS_FEED_DB_ALIAS,
    ARTICLES_A_DB_ALIAS,
    ARTICLES_B_DB_ALIAS,
    ARTICLES_C_DB_ALIAS,
)
from core import BASE_DIR


env_path = os.path.join(BASE_DIR, ".env")
load_env(env_path)


def main():
    """Run migrate for all databases."""

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    print("Run migrate for all databases")

    production_env = bool(int(get_env_value("PROD")))
    settings_path = get_settings_path(prod=production_env)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_path)

    print(f"{settings_path} environment")

    script = "manage.py"
    command = "migrate"
    flag = "--database"

    # Migrate for all databases (commands).
    execute_from_command_line([script, command, f"{flag}={AUTH_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={NEWS_FEED_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_A_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_B_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_C_DB_ALIAS}"])


if __name__ == "__main__":
    main()
