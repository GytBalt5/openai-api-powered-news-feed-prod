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


def determine_expected_database_based_on_modulo_sharding(uid: int, shards: list):
   return shards[uid % len(shards)]


class DBRouterShardingTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase."""
        cls.article_router = ArticleRouter()
        cls.expected_db_alias = [ARTICLES_A_DB_ALIAS, ARTICLES_B_DB_ALIAS, ARTICLES_C_DB_ALIAS]
        cls.articles_amount = 22

    def test_db_alias_list(self):
        """Router db list should match the expected list."""
        self.assertEqual(self.expected_db_alias, self.article_router.db_alias)

    def test_db_for_write(self):
        """Router should select the correct db for write."""
        for fake_uid in range(1, self.articles_amount + 1):
            expected_db = determine_expected_database_based_on_modulo_sharding(
                fake_uid, self.expected_db_alias
            )
            selected_db = self.article_router.db_for_write(Article, hints={"uid": fake_uid})
            self.assertEqual(expected_db, selected_db)

    def test_db_for_read(self):
        """Router should select the correct db for read."""
        for fake_uid in range(1, self.articles_amount + 1):
            expected_db = determine_expected_database_based_on_modulo_sharding(
                fake_uid, self.expected_db_alias
            )
            selected_db = self.article_router.db_for_read(Article, hints={"uid": fake_uid})
            self.assertEqual(expected_db, selected_db)

    def test_allow_migrate(self):
        """Router should have correct permissions for allow_migrate."""
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

    def test_select_db_no_hints(self):
        """Router should select the correct db without hints."""
        # Evaluate default selection for write operations.
        selected_db = self.article_router.db_for_write(Article)
        self.assertEqual(ARTICLES_A_DB_ALIAS, selected_db)

        # Evaluate default selection for read operations.
        selected_db = self.article_router.db_for_read(Article)
        self.assertEqual(ARTICLES_A_DB_ALIAS, selected_db)
