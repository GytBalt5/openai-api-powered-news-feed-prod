from core.utils import (
    AUTH_DB_ALIAS,
    NEWS_FEED_DB_ALIAS,
    ARTICLES_A_DB_ALIAS,
    ARTICLES_B_DB_ALIAS,
    ARTICLES_C_DB_ALIAS,
)


def determine_expected_shard_with_modulo_sharding(uid: int, shards: list) -> str:
    """
    Determine the expected shard for a given UID using modulo sharding logic.
    Args:
        uid (int): The unique identifier for which the shard needs to be determined.
        shards (list): A list of available shards.
    Returns:
        str: The determined shard for the given UID.
    """
    # Calculate the shard index using modulo operation.
    shard_index = uid % len(shards)
    return shards[shard_index]


class BaseRouter:
    """
    A base router for custom database routing.
    This router provides the basic functionality for routing database operations
    based on the model's app label.
    """

    route_app_labels = set()  # app labels that this router handles
    db_alias = None  # the database alias for this router

    def db_for_read(self, model, **hints):
        """Determine the database to use for reading."""
        return self._select_db(model, **hints)

    def db_for_write(self, model, **hints):
        """Determine the database to use for writing."""
        return self._select_db(model, **hints)

    def allow_migrate(self, db, app_label, **hints):
        """Determine if migration is allowed."""
        return db == self.db_alias if app_label in self.route_app_labels else None

    def allow_relation(self, obj1, obj2, **hints):
        """Determine if a relation between objects is allowed."""
        return (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        )

    def _select_db(self, model, **hints):
        """Select the appropriate database based on the model's app label."""
        return self.db_alias if model._meta.app_label in self.route_app_labels else None


class AuthRouter(BaseRouter):
    """
    Router for authentication and user-related operations.
    Routes operations for user management, authentication, and related admin tasks.
    """

    route_app_labels = {"users", "auth", "contenttypes", "admin", "sessions"}
    db_alias = AUTH_DB_ALIAS


class NewsFeedRouter(BaseRouter):
    """
    Router for news-feed-related operations.
    Handles operations related to news_feed management and associated admin tasks.
    """

    route_app_labels = {"news_feed", "contenttypes", "admin"}
    db_alias = NEWS_FEED_DB_ALIAS


class ArticleRouter(BaseRouter):
    """
    Router for article-related operations with sharding logic.
    This router implements sharding logic to distribute article data across multiple databases.
    """

    route_app_labels = {"articles", "contenttypes", "admin"}
    db_alias = [ARTICLES_A_DB_ALIAS, ARTICLES_B_DB_ALIAS, ARTICLES_C_DB_ALIAS]

    def allow_migrate(self, db, app_label, **hints):
        """Determine if migration is allowed for sharded databases."""
        if app_label in self.route_app_labels:
            return db in self.db_alias
        return None

    def _select_db(self, model, **hints):
        """Select the appropriate shard based on the model's app label and hints."""
        return (
            self._get_shard(**hints)
            if model._meta.app_label in self.route_app_labels
            else None
        )

    def _get_shard(self, **hints):
        """
        Determine the appropriate shard for the given hints.
        If a unique ID (uid) is provided in the hints, it's used to determine the shard.
        Otherwise, defaults to the first shard.
        """
        assert isinstance(self.db_alias, list)
        assert len(self.db_alias) > 0, f"db_alias must be provided {self.db_alias}"

        uid = hints.get("hints", {}).get("uid")
        if uid:
            return determine_expected_shard_with_modulo_sharding(uid, self.db_alias)

        # Default to the first shard if uid is not provided.
        return self.db_alias[0]
