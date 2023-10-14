import graphene

from news_feed.queries import Query
from news_feed.mutations import Mutation


schema = graphene.Schema(query=Query, mutation=Mutation)
