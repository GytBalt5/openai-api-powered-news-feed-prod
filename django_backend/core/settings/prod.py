from datetime import timedelta

from core.settings.base import *
from core.utils import (
    get_multi_databases_config,
    get_db_routers,
    get_google_secretmanager_secrets,
    get_secret,
)


# Google secret manager secret info.
SECRETS = get_google_secretmanager_secrets()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret(SECRETS, "APP_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Cross-origin resource sharing.
CORS_ORIGIN_ALLOW_ALL = False

# Databases.
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = get_multi_databases_config(env="prod", secrets=SECRETS)

# Database routers for which of our DBs to use for what.
DATABASE_ROUTERS = get_db_routers()

# Media Files.
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = get_secret(SECRETS, "BUCKET_NAME")
GS_FILE_OVERWRITE = False
MEDIA_ROOT = "https://storage.googleapis.com/{}".format(GS_BUCKET_NAME)
MEDIA_URL = "/media/"
GS_EXPIRATION = timedelta(minutes=2)
