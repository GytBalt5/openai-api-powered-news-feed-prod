from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType

from news_feed.models import Category, Site
from articles.models import Article


User = get_user_model()


class SiteType(DjangoObjectType):
    class Meta:
        model = Site


class UserType(DjangoObjectType):
    class Meta:
        model = User


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
