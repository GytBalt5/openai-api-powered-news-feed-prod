#!/usr/bin/env python
import os
from pathlib import Path

from utils.utils import get_settings_path
from core.utils.database_config import (
    AUTH_DB_ALIAS,
    NEWS_FEED_DB_ALIAS,
    ARTICLES_A_DB_ALIAS,
    ARTICLES_B_DB_ALIAS,
    ARTICLES_C_DB_ALIAS,
)


BASE_DIR = Path(__file__).resolve().parent


def main():
    """Setup for test databases."""

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.settings_for_tests")

    script = "manage.py"
    flag = "--database"

    # Reset all databases (commands).
    command = "reset_db"
    execute_from_command_line([script, command, f"{flag}={AUTH_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={NEWS_FEED_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_A_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_B_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_C_DB_ALIAS}"])

    # Make migrations.
    command = "makemigrations"
    execute_from_command_line([script, command])

    # Migrate for all databases (commands).
    command = "migrate"
    execute_from_command_line([script, command, f"{flag}={AUTH_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={NEWS_FEED_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_A_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_B_DB_ALIAS}"])
    execute_from_command_line([script, command, f"{flag}={ARTICLES_C_DB_ALIAS}"])


if __name__ == "__main__":
    main()
