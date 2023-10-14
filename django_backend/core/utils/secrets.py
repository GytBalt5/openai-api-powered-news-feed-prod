import os
import json
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from core.utils.dotenv import load_env, get_env_value

from google.cloud import secretmanager
from google.oauth2 import service_account


BASE_DIR = Path(__file__).resolve().parent.parent.parent

env_path = os.path.join(BASE_DIR, ".env")
load_env(env_path)


def get_google_secretmanager_secrets():
    # GCP project in which to store secrets in Secret Manager.
    google_project_id = get_env_value("BL_GOOGLE_PROJECT_ID")
    # ID of the secret to create.
    google_secret_manager_id = get_env_value("BL_GOOGLE_SECRET_MANAGER_ID")

    # Create the Secret Manager client.
    credentials_path = os.path.join(
        os.path.join(BASE_DIR.parent, "creds"), get_env_value("BL_GOOGLE_CREDENTIALS")
    )
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    secretmanager_client = secretmanager.SecretManagerServiceClient(
        credentials=credentials
    )

    secrets = secretmanager_client.access_secret_version(
        name=f"projects/{google_project_id}/secrets/{google_secret_manager_id}/versions/1"
    ).payload.data.decode("UTF-8")

    return json.loads(secrets)


def get_secret(secrets, key):
    try:
        return secrets.get(key)
    except KeyError:
        error_msg = "Incorrect secret name"
        raise ImproperlyConfigured(error_msg)
