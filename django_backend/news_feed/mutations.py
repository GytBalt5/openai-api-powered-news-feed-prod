"""
*** Mutation sends data to the database.
"""

from django.contrib.auth import get_user_model

import graphene
import graphql_jwt
from graphene_file_upload.scalars import Upload

from news_feed.models import Topic
from news_feed.types import UserType, ArticleType
from articles.models import Article


User = get_user_model()


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    """
    Customize the ObtainJSONWebToken behavior to include the user info.
    """

    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class UpdateUserProfile(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        user_id = graphene.ID(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        avatar = Upload(required=False)
        bio = graphene.String(required=False)
        location = graphene.String(required=False)
        website = graphene.String(required=False)

    def mutate(
        self,
        info,
        user_id,
        first_name="",
        last_name="",
        avatar="",
        bio="",
        location="",
        website="",
    ):
        user = User.objects.get(pk=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.avatar = avatar
        user.bio = bio
        user.location = location
        user.website = website
        user.save()

        return UpdateUserProfile(user=user)


class CreateArticle(graphene.Mutation):
    article = graphene.Field(ArticleType)

    class Arguments:
        user_id = graphene.ID(required=True)
        topic_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        is_published = graphene.Boolean(required=True)
        is_featured = graphene.Boolean(required=True)

    def mutate(
        self, info, user_id, topic_id, title, content, is_published, is_featured
    ):
        user_id = User.objects.get(id=user_id).id
        topic_id = Topic.objects.get(id=topic_id).id
        article_obj = Article.objects.create(
            user_id=user_id,
            topic_id=topic_id,
            title=title,
            content=content,
            is_published=is_published,
            is_featured=is_featured,
        )
        return CreateArticle(article=article_obj)


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_user = CreateUser.Field()
    update_user_profile = UpdateUserProfile.Field()

    create_article = CreateArticle.Field()
