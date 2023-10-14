# Configure GraphQL.
GRAPHENE = {
    "SCHEMA": "news_feed.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}
