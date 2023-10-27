import random

from django.test import TestCase

from users.utils import create_super_user
from news_feed.utils import create_category
from articles.utils import create_article
from articles.models import Article
from core.utils.routers import ArticleRouter
from core.utils.database_config import ARTICLES_DB_SHARDS


def random_topic_id(topics: list) -> int:
    """
    Return a random topic id from the given topics list.
    """
    return random.choice(topics)


class ArticlesDBShardingBaseTestCase(TestCase):
    databases = "__all__"

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.
        """
        cls.article_router = ArticleRouter()
        cls.article_count = 22
        cls.articles = []
        cls.user_id = create_super_user().id

        cls.topics = [
            create_category(name=f"Name{idx + 1}", description=f"Desc{idx + 1}").id
            for idx in range(len(ARTICLES_DB_SHARDS))
        ]

    def setUp(self):
        """
        Set up test environment for each test method.
        """
        for idx in range(1, self.article_count + 1):
            self.articles.append(
                create_article(
                    title=f"ARTICLE {idx + 1}",
                    content=f"ARTICLE {idx + 1}",
                    is_featured=True,
                    is_published=True,
                    topic_id=random_topic_id(self.topics),
                    user_id=self.user_id,
                )
            )

    def tearDown(self):
        """
        Clean up after each test method.
        """
        Article.objects.all().delete()


class DBShardingCRUDTestCase(ArticlesDBShardingBaseTestCase):
    def test_should_return_random_topic_id(self):
        """
        Should random topic id exists in topics list.
        """
        topic_id = random_topic_id(self.topics)
        self.assertIn(topic_id, self.topics)
        topic_id = random_topic_id(self.topics)
        self.assertIn(topic_id, self.topics)
        topic_id = random_topic_id(self.topics)
        self.assertIn(topic_id, self.topics)

    def test_should_be_created_articles_of_amount(self):
        """
        Should create articles of amount as the expected amount.
        """
        self.assertEqual(self.article_count, len(self.articles))
        total_articles = sum(
            Article.objects.using(db_alias).count()
            for db_alias in self.article_router.db_alias
        )
        self.assertEqual(self.article_count, total_articles)

    def test_should_create_articles(self):
        """
        Should save each article to the expected shard.
        """
        user_id = create_super_user().id
        for idx in range(1, self.article_count):
            p = create_article(
                title=f"ARTICLE {idx + 1}",
                content=f"ARTICLE {idx + 1}",
                is_featured=True,
                is_published=True,
                topic_id=random_topic_id(self.topics),
                user_id=user_id,
            )
            expected_db = self.article_router.db_for_write(
                Article, hints={"topic_id": p.topic_id}
            )
            self.assertEqual(expected_db, p._state.db)

    def test_should_retrieve_articles(self):
        """
        Should retrieve each article from the expected shard.
        """
        for article in self.articles:
            expected_db = self.article_router.db_for_read(
                Article, hints={"topic_id": article.topic_id}
            )
            retrieved_article = (
                Article.objects.using(expected_db).filter(uid=article.uid).first()
            )
            self.assertIsNotNone(retrieved_article)
            self.assertEqual(article.uid, retrieved_article.uid)

    def test_should_articles_update(self):
        """
        Should update each article in the expected shard.
        """
        for article in self.articles:
            expected_title = f"Updated Title {article.uid}"
            article.title = expected_title
            article.save()
            expected_db = self.article_router.db_for_read(
                Article, hints={"topic_id": article.topic_id}
            )
            updated_article = (
                Article.objects.using(expected_db).filter(uid=article.uid).first()
            )
            self.assertIsNotNone(updated_article)
            self.assertEqual(expected_title, updated_article.title)

    def test_should_articles_delete(self):
        """
        Should delete each article from the expected shard.
        """
        for article in self.articles:
            expected_db = self.article_router.db_for_read(
                Article, hints={"topic_id": article.topic_id}
            )
            article.delete()
            self.assertFalse(
                Article.objects.using(expected_db).filter(uid=article.uid).exists()
            )
        total_articles = sum(
            Article.objects.using(db_alias).count()
            for db_alias in self.article_router.db_alias
        )
        self.assertEqual(0, total_articles)


class DBShardingCRUDAutoSelectingDBTestCase(ArticlesDBShardingBaseTestCase):
    """
    NOTE. DB should be auto selected.
    """

    def test_should_be_created_articles_of_amount_auto(self):
        """
        Should create articles of amount as the expected amount.
        """
        self.assertEqual(self.article_count, len(self.articles))
        self.assertEqual(self.article_count, Article.objects.count())

    def test_should_retrieve_articles_auto(self):
        """
        Should retrieve articles.
        """
        for article in self.articles:
            retrieved_article = Article.objects.filter(uid=article.uid).first()
            self.assertIsNotNone(retrieved_article)
            self.assertEqual(article.uid, retrieved_article.uid)

    def test_should_articles_update_auto(self):
        """
        Should correctly update articles.
        """
        for article in self.articles:
            expected_title = f"Updated Title {article.uid}"
            article.title = expected_title
            article.save()
            updated_article = Article.objects.filter(uid=article.uid).first()
            self.assertIsNotNone(updated_article)
            self.assertEqual(expected_title, updated_article.title)

    def test_should_articles_delete_auto(self):
        """
        Should delete articles.
        """
        for article in self.articles:
            article_uid = article.uid
            article.delete()
            self.assertFalse(Article.objects.filter(uid=article_uid).exists())
        self.assertEqual(0, Article.objects.count())
