from django.contrib.auth import get_user_model

import graphene

from articles.models import Article
from news_feed.models import Site, Category
from news_feed.types import ArticleType, CategoryType, UserType, SiteType


User = get_user_model()


class Query(graphene.ObjectType):
    site = graphene.Field(SiteType)
    current_user = graphene.Field(UserType, username=graphene.String())

    all_articles = graphene.List(ArticleType)
    articles_by_category = graphene.List(ArticleType, category=graphene.String())
    articles_by_user = graphene.List(ArticleType, username=graphene.String())
    article_by_slug = graphene.Field(ArticleType, slug=graphene.String())

    all_categories = graphene.List(CategoryType)

    def resolve_site(self, info):
        return Site.objects.first()

    def resolve_all_articles(self, info):
        return Article.objects.all()

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_articles_by_category(self, info, category):
        category_id = Category.objects.get(slug__iexact=category).id
        return Article.objects.filter(category_id=category_id).all()

    def resolve_articles_by_user(self, info, username):
        user_id = User.objects.get(username__iexact=username).id
        return Article.objects.filter(user_id=user_id).all()

    def resolve_article_by_slug(self, info, slug):
        return Article.objects.get(slug__iexact=slug)

    def resolve_current_user(self, info, username):
        return User.objects.get(username__iexact=username)
