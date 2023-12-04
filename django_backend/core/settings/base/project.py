import os

from core.utils.dotenv import load_env, get_env_value
from core import BASE_DIR


PROJECT_ROOT = BASE_DIR.parent
VUE_FRONTEND_DIR = os.path.join(PROJECT_ROOT, "vue_frontend")
VUE_STATIC_DIR = os.path.join(VUE_FRONTEND_DIR, "dist")

# Load environment variables from the .env file
env_path = os.path.join(BASE_DIR, ".env")
load_env(env_path)

# Define default allowed hosts and extend with any remote allowed hosts from environment variables.
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS.extend(filter(None, get_env_value("REMOTE_ALLOWED_HOST")))

# Define default CORS origins and extend with any remote origins from environment variables.
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
CORS_ORIGIN_WHITELIST.extend(
    filter(None, get_env_value("REMOTE_CORS_ORIGIN_WHITELIST"))
)

# Define password validation rules.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Define the URL path for serving static files.
STATIC_URL = "static/"

STATICFILES_DIRS = [
    VUE_STATIC_DIR,
]

# Define the default primary key field type for models.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Define the upload path for CKEditor.
CKEDITOR_UPLOAD_PATH = "articles/uploads/%Y/%m/%d/"

# Set the custom user model.
AUTH_USER_MODEL = "users.CustomUser"

# Define authentication backends, including JWT for GraphQL.
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Define custom migration modules for apps.
MIGRATION_MODULES = {
    "users": "core.all_migrations.users",
    "news_feed": "core.all_migrations.news_feed",
    "articles": "core.all_migrations.articles",
}
