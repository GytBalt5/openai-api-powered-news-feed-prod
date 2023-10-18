import os

from core.settings.base import *
from core.utils import get_multi_databases_config_for_tests, get_db_routers


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "TESTAS1231231231TESTAS00000000000000000000000000000000001"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Cross-origin resource sharing.
CORS_ORIGIN_ALLOW_ALL = True

# Databases.
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = get_multi_databases_config_for_tests()

# Database routers for which of our DBs to use for what.
DATABASE_ROUTERS = get_db_routers()

# Media Files.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Setting for a dev env default superuser creds.
DJANGO_SUPERUSER_USERNAME = "admin"
DJANGO_SUPERUSER_PASSWORD = "testtest1231"

# Disable logging during tests.
LOGGING_CONFIG = None
