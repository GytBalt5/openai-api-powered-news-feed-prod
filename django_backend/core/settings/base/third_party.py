import os

from core.utils.dotenv import load_env, get_env_value
from core import BASE_DIR


# Load environment variables from the .env file.
env_path = os.path.join(BASE_DIR, ".env")
load_env(env_path)

# Configure GraphQL.
GRAPHENE = {
    "SCHEMA": "news_feed.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

# TODO. Maybe need to obtain differently for dev. and prod. in future.
# OpenAI API key.
OPENAI_API_KEY = get_env_value("OPENAI_API_KEY")
