import os
from pathlib import Path

from core.utils.dotenv import load_env, get_env_value
from core.utils.secrets import get_secret


BASE_DIR = Path(__file__).resolve().parent.parent.parent

AUTH_DB_ALIAS = "default"
NEWS_FEED_DB_ALIAS = "news_feed_db"

# Three shards.
ARTICLES_A_DB_ALIAS = "articles_a_db"
ARTICLES_B_DB_ALIAS = "articles_b_db"
ARTICLES_C_DB_ALIAS = "articles_c_db"


def get_multi_databases_config(env=None, secrets=None):
    """
    Return the DATABASES configuration based on the environment.
    """
    if secrets is None:
        env_path = os.path.join(BASE_DIR, ".env")
        load_env(env_path)

    db_engine = "django.db.backends.mysql"
    db_name_postfix = "_prod" if env == "prod" else "_dev"

    db_user = _get_secret_for_db(secrets, "DB_USER")
    db_password = _get_secret_for_db(secrets, "DB_PASSWORD")
    db_host = _get_secret_for_db(secrets, "DB_HOST")
    db_port = int(_get_secret_for_db(secrets, "DB_PORT"))

    # Database aliases mapped to their names.
    db_names = {
        AUTH_DB_ALIAS: "auth_db",
        NEWS_FEED_DB_ALIAS: NEWS_FEED_DB_ALIAS,
        ARTICLES_A_DB_ALIAS: ARTICLES_A_DB_ALIAS,
        ARTICLES_B_DB_ALIAS: ARTICLES_B_DB_ALIAS,
        ARTICLES_C_DB_ALIAS: ARTICLES_C_DB_ALIAS,
    }

    return {
        alias: _get_db_value(
            db_engine, name + db_name_postfix, db_user, db_password, db_host, db_port
        )
        for alias, name in db_names.items()
    }


def get_multi_databases_config_for_tests():
    """
    Return the DATABASES configuration for tests.
    """
    db_engine = "django.db.backends.sqlite3"

    db_names = {
        AUTH_DB_ALIAS: "test_auth_db",
        NEWS_FEED_DB_ALIAS: f"test_{NEWS_FEED_DB_ALIAS}",
        ARTICLES_A_DB_ALIAS: f"test_{ARTICLES_A_DB_ALIAS}",
        ARTICLES_B_DB_ALIAS: f"test_{ARTICLES_B_DB_ALIAS}",
        ARTICLES_C_DB_ALIAS: f"test_{ARTICLES_C_DB_ALIAS}",
    }

    dbs_dir = os.path.join(BASE_DIR, "sqlite3")

    return {
        alias: {
            "ENGINE": db_engine,
            "NAME": os.path.join(dbs_dir, name),
        }
        for alias, name in db_names.items()
    }


def get_db_routers():
    return [
        "core.utils.router.AuthRouter",
        "core.utils.router.NewsFeedRouter",
        "core.utils.router.ArticleRouter",
    ]


def _get_db_value(engine, name, user, passwd, host, port):
    return {
        "ENGINE": engine,
        "NAME": name,
        "USER": user,
        "PASSWORD": passwd,
        "HOST": host,
        "PORT": port,
    }


def _get_secret_for_db(secrets, key):
    return get_secret(secrets, key) if secrets else get_env_value(key)
