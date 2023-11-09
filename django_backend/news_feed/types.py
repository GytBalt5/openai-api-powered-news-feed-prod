from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType

from news_feed.models import Topic, Site
from articles.models import Article


User = get_user_model()


class SiteType(DjangoObjectType):
    class Meta:
        model = Site


class UserType(DjangoObjectType):
    class Meta:
        model = User


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
