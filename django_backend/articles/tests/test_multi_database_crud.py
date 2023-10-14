from django.test import TestCase

from users.utils import create_super_user
from news_feed.utils import create_category
from articles.utils import create_article
from articles.models import Article
from core.utils.router import ArticleRouter


class ArticlesDBShardingBaseTestCase(TestCase):

    databases = "__all__"

    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase."""
        cls.article_router = ArticleRouter()
        cls.article_count = 22
        cls.articles = []
        cls.article_category_id = create_category("GENERAL-ARTICLE", "General articles").id
        cls.user_id = create_super_user().id

    def setUp(self):
        """Set up test environment for each test method."""
        for idx in range(1, self.article_count + 1):
            self.articles.append(
                create_article(
                    title=f"ARTICLE {idx + 1}",
                    content=f"ARTICLE {idx + 1}",
                    is_featured=True,
                    is_published=True,
                    category_id=self.article_category_id,
                    user_id=self.user_id,
                )
            )

    def tearDown(self):
        """Clean up after each test method."""
        Article.objects.all().delete()


class DBShardingCRUDTestCase(ArticlesDBShardingBaseTestCase):

    def test_articles_amount(self):
        """Should create articles of amount as the expected amount."""
        self.assertEqual(self.article_count, len(self.articles))
        total_articles = sum(
            Article.objects.using(db_alias).count()
            for db_alias in self.article_router.db_alias
        )
        self.assertEqual(self.article_count, total_articles)

    def test_data_creation(self):
        """Should save each article to the expected shard."""
        article_category_id = create_category("GENERAL-ARTICLE", "General articles").id
        user_id = create_super_user().id
        for idx in range(1, self.article_count):
            p = create_article(
                title=f"ARTICLE {idx + 1}",
                content=f"ARTICLE {idx + 1}",
                is_featured=True,
                is_published=True,
                category_id=article_category_id,
                user_id=user_id,
            )
            expected_db = self.article_router.db_for_write(Article, hints={"uid": p.uid})
            self.assertEqual(expected_db, p._state.db)

    def test_data_retrieval(self):
        """Should retrieve each article from the expected shard."""
        for article in self.articles:
            expected_db = self.article_router.db_for_read(Article, hints={"uid": article.uid})
            retrieved_article = (
                Article.objects.using(expected_db).filter(uid=article.uid).first()
            )
            self.assertIsNotNone(retrieved_article)
            self.assertEqual(article.uid, retrieved_article.uid)

    def test_data_update(self):
        """Should update each article in the expected shard."""
        for article in self.articles:
            expected_title = f"Updated Title {article.uid}"
            article.title = expected_title
            article.save()
            expected_db = self.article_router.db_for_read(Article, hints={"uid": article.uid})
            updated_article = Article.objects.using(expected_db).get(uid=article.uid)
            self.assertEqual(expected_title, updated_article.title)

    def test_data_deletion(self):
        """Should delete each article from the expected shard."""
        for article in self.articles:
            article_uid = article.uid
            expected_db = self.article_router.db_for_read(Article, hints={"uid": article_uid})
            article.delete()
            self.assertFalse(
                Article.objects.using(expected_db).filter(uid=article_uid).exists()
            )
        total_articles = sum(
            Article.objects.using(db_alias).count()
            for db_alias in self.article_router.db_alias
        )
        self.assertEqual(0, total_articles)


class DBShardingCRUDAutoSelectingDBTestCase(ArticlesDBShardingBaseTestCase):

    def test_articles_amount(self):
        """
        Note. DB should be auto selected.
        Should create the correct number of articles.
        """
        self.assertEqual(self.article_count, len(self.articles))
        self.assertEqual(self.article_count, Article.objects.count())

    def test_data_retrieval(self):
        """
        Note. DB should be auto selected.
        Should correctly retrieve articles.
        """
        for article in self.articles:
            retrieved_article = Article.objects.filter(uid=article.uid).first()
            self.assertIsNotNone(retrieved_article)
            self.assertEqual(article.uid, retrieved_article.uid)

    def test_data_update(self):
        """
        Note. DB should be auto selected.
        Should correctly update articles.
        """
        for article in self.articles:
            expected_title = f"Updated Title {article.uid}"
            article.title = expected_title
            article.save()
            updated_article = Article.objects.filter(uid=article.uid).first()
            self.assertIsNotNone(updated_article)
            self.assertEqual(expected_title, updated_article.title)

    def test_data_deletion(self):
        """
        Note. DB should be auto selected.
        Should correctly delete articles.
        """
        for article in self.articles:
            article_uid = article.uid
            article.delete()
            self.assertFalse(Article.objects.filter(uid=article_uid).exists())
        self.assertEqual(0, Article.objects.count())
