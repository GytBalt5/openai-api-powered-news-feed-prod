from django.test import TestCase

from articles.models import Article
from core.utils.router import ArticleRouter
from core.utils import (
    ARTICLES_A_DB_ALIAS,
    ARTICLES_B_DB_ALIAS,
    ARTICLES_C_DB_ALIAS,
    AUTH_DB_ALIAS,
    NEWS_FEED_DB_ALIAS,
)


def determine_expected_database_with_modulo_sharding(uid: int, shards: list):
    # Create a mapping of shard index to shard name.
    shard_mappings = {index: shard for index, shard in enumerate(shards)}
    # Use modulo operation to determine the shard for the given UID.
    return shard_mappings[uid % len(shards)]


class DBRouterShardingTestCase(TestCase):
    def setUp(self):
        """Set up the test environment with the router, expected database aliases, and shard count."""
        self.article_router = ArticleRouter()
        self.expected_db_alias = [ARTICLES_A_DB_ALIAS, ARTICLES_B_DB_ALIAS, ARTICLES_C_DB_ALIAS]
        self.articles_amount = 22

    def test_should_be_equal_router_db_list_as_expected_list(self):
        """Ensure that the router's database aliases correspond to the expected list."""
        self.assertEqual(self.expected_db_alias, self.article_router.db_alias)

    def test_should_router_select_correct_db_for_write(self):
        """Check if the router correctly selects the database for write operations based on article UID."""
        for fake_uid in range(1, self.articles_amount + 1):
            expected_db = determine_expected_database_with_modulo_sharding(
                fake_uid, self.expected_db_alias
            )
            selected_db = self.article_router.db_for_write(Article, hints={"uid": fake_uid})
            self.assertEqual(expected_db, selected_db)

    def test_should_router_select_correct_db_for_read(self):
        """Check if the router correctly selects the database for read operations based on article UID."""
        for fake_uid in range(1, self.articles_amount + 1):
            expected_db = determine_expected_database_with_modulo_sharding(
                fake_uid, self.expected_db_alias
            )
            selected_db = self.article_router.db_for_read(Article, hints={"uid": fake_uid})
            self.assertEqual(expected_db, selected_db)

    def test_should_router_have_correct_permissions_for_allow_migrate(self):
        """Evaluate the router's migration permissions across various app labels and databases."""
        # Check permissions for expected app labels.
        for db in self.expected_db_alias:
            self.assertTrue(self.article_router.allow_migrate(db=db, app_label="articles"))
            self.assertTrue(self.article_router.allow_migrate(db=db, app_label="contenttypes"))
            self.assertTrue(self.article_router.allow_migrate(db=db, app_label="admin"))
            self.assertIsNone(self.article_router.allow_migrate(db=db, app_label="users"))
            self.assertIsNone(self.article_router.allow_migrate(db=db, app_label="news_feed"))
            self.assertIsNone(self.article_router.allow_migrate(db=db, app_label="some_app"))

        # Check permissions for databases not related to article operations.
        for db in [AUTH_DB_ALIAS, NEWS_FEED_DB_ALIAS, "some_db"]:
            self.assertFalse(self.article_router.allow_migrate(db=db, app_label="articles"))
            self.assertFalse(self.article_router.allow_migrate(db=db, app_label="contenttypes"))
            self.assertFalse(self.article_router.allow_migrate(db=db, app_label="admin"))
            self.assertIsNone(self.article_router.allow_migrate(db=db, app_label="users"))
            self.assertIsNone(self.article_router.allow_migrate(db=db, app_label="news_feed"))
            self.assertIsNone(self.article_router.allow_migrate(db=db, app_label="some_app"))

    def test_should_router_select_correct_db_without_hints(self):
        """Assess the router's default database selection in the absence of hints."""
        # Evaluate default selection for write operations.
        selected_db = self.article_router.db_for_write(Article)
        self.assertEqual(ARTICLES_A_DB_ALIAS, selected_db)

        # Evaluate default selection for read operations.
        selected_db = self.article_router.db_for_read(Article)
        self.assertEqual(ARTICLES_A_DB_ALIAS, selected_db)
