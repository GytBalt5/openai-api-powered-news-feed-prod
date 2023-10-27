from core.utils.database_config import (
    get_multi_databases_config,
    get_multi_databases_config_for_tests,
    get_db_routers,
    AUTH_DB_ALIAS,
    NEWS_FEED_DB_ALIAS,
    ARTICLES_A_DB_ALIAS,
    ARTICLES_B_DB_ALIAS,
    ARTICLES_C_DB_ALIAS,
    ARTICLES_DB_SHARDS,
)
from core.utils.secrets import get_google_secretmanager_secrets, get_secret
