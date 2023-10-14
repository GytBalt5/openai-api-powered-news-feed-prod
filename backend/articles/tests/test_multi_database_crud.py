from django.test import TestCase

from core.utils.router import ArticleRouter
from users.utils import create_super_user
from articles.models import Article
from news_feed.utils import create_category
from articles.utils import create_article


class DBShardingCRUDTestCase(TestCase):
    databases = "__all__"

    def setUp(self):
        """Set up test environment with articles, categories, and users."""
        self.article_router = ArticleRouter()
        self.article_count = 22
        self.articles = []
        article_category_id = create_category("GENERAL-ARTICLE", "General articles").id
        user_id = create_super_user().id
        for idx in range(1, self.article_count + 1):
            self.articles.append(
                create_article(
                    title=f"ARTICLE {idx + 1}",
                    content=f"ARTICLE {idx + 1}",
                    is_featured=True,
                    is_published=True,
                    category_id=article_category_id,
                    user_id=user_id,
                )
            )

    def test_articles_amount(self):
        """Ensure the correct number of articles are created and distributed across databases."""
        self.assertEqual(self.article_count, len(self.articles))
        total_articles = sum(
            Article.objects.using(db_alias).count()
            for db_alias in self.article_router.db_alias
        )
        self.assertEqual(self.article_count, total_articles)

    def test_data_creation(self):
        """Validate that each article is saved in the expected shard."""
        article_category_id = create_category("GENERAL-ARTICLE", "General articles").id
        user_id = create_super_user().id
        temp_articles = []
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
            temp_articles.append(p)

        # Clean up temporary articles after test.
        for article in temp_articles:
            article.delete()

    def test_data_retrieval(self):
        """Test if data can be correctly retrieved from the expected database."""
        for article in self.articles:
            expected_db = self.article_router.db_for_read(Article, hints={"uid": article.uid})
            retrieved_article = (
                Article.objects.using(expected_db).filter(uid=article.uid).first()
            )
            self.assertIsNotNone(retrieved_article)
            self.assertEqual(article.uid, retrieved_article.uid)

    def test_data_update(self):
        """Test if data can be correctly updated in the expected database."""
        for article in self.articles:
            expected_title = f"Updated Title {article.uid}"
            article.title = expected_title
            article.save()
            expected_db = self.article_router.db_for_read(Article, hints={"uid": article.uid})
            updated_article = Article.objects.using(expected_db).get(uid=article.uid)
            self.assertEqual(expected_title, updated_article.title)

    def test_data_deletion(self):
        """Test if data can be correctly deleted from the expected database."""
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


class DBShardingCRUDAutoSelectingDBTestCase(TestCase):
    databases = "__all__"

    def setUp(self):
        """Set up test environment with articles, categories, and users."""
        self.article_router = ArticleRouter()
        self.article_count = 22
        self.articles = []
        article_category_id = create_category("GENERAL-ARTICLE", "General articles").id
        user_id = create_super_user().id
        for idx in range(1, self.article_count + 1):
            self.articles.append(
                create_article(
                    title=f"ARTICLE {idx + 1}",
                    content=f"ARTICLE {idx + 1}",
                    is_featured=True,
                    is_published=True,
                    category_id=article_category_id,
                    user_id=user_id,
                )
            )

    def test_articles_amount(self):
        """Ensure the correct number of articles are created."""
        self.assertEqual(self.article_count, len(self.articles))
        self.assertEqual(self.article_count, Article.objects.count())

    def test_data_retrieval_auto_selecting_db(self):
        """Test if data can be correctly retrieved without explicitly selecting the database."""
        for article in self.articles:
            retrieved_article = Article.objects.filter(uid=article.uid).first()
            self.assertIsNotNone(retrieved_article)
            self.assertEqual(article.uid, retrieved_article.uid)

    def test_data_update_auto_selecting_db(self):
        """Test if data can be correctly updated without explicitly selecting the database."""
        for article in self.articles:
            expected_title = f"Updated Title {article.uid}"
            article.title = expected_title
            article.save()
            updated_article = Article.objects.filter(uid=article.uid).first()
            self.assertIsNotNone(updated_article)
            self.assertEqual(expected_title, updated_article.title)

    def test_data_deletion_auto_selecting_db(self):
        """Test if data can be correctly deleted without explicitly selecting the database."""
        for article in self.articles:
            article_uid = article.uid
            article.delete()
            self.assertFalse(Article.objects.filter(uid=article_uid).exists())
        self.assertEqual(0, Article.objects.count())
