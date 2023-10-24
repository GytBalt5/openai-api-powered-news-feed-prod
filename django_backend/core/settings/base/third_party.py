import os
from pathlib import Path

from core.utils.dotenv import load_env, get_env_value


# Determine the base directory of the project.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

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
