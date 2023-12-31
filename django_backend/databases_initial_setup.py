#!/usr/bin/env python
import os
from pathlib import Path

import django

from core.utils.dotenv import load_env, get_env_value
from utils.general import get_settings_path
from core import BASE_DIR


env_path = os.path.join(BASE_DIR, ".env")
load_env(env_path)

PRODUCTION_ENV = bool(int(get_env_value("PROD")))
SETTINGS_PATH = get_settings_path(prod=PRODUCTION_ENV)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_PATH)

django.setup()


from users.utils import create_super_user
from news_feed.utils import create_topic
from articles.utils import create_article


def db_init_setup(user_id):
    print("user_id: ", user_id)
    a_article_topic_id = create_topic("A-ART", "AArt db articles").id
    b_article_topic_id = create_topic("B-ART", "BArt db articles").id
    c_article_topic_id = create_topic("C-ART", "CArt db articles").id
    print(
        "topic ids: ",
        a_article_topic_id,
        b_article_topic_id,
        c_article_topic_id,
    )

    for idx, topic_id in enumerate(
        [
            a_article_topic_id,
            b_article_topic_id,
            c_article_topic_id,
            a_article_topic_id,
            b_article_topic_id,
            c_article_topic_id,
            a_article_topic_id,
            b_article_topic_id,
            c_article_topic_id,
            a_article_topic_id,
            b_article_topic_id,
            c_article_topic_id,
        ]
    ):
        p = create_article(
            title=f"ARTICLE {idx + 1}",
            content=f"ARTICLE {idx + 1}",
            is_featured=True,
            is_published=True,
            topic_id=topic_id,
            user_id=user_id,
        )
        print(f"Article created: {p}")


def main(settings):
    """Run initial database setup (add records)"""

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    print(f"{settings} environment")
    print("Initial databases setup (add records)")

    if settings == "core.settings.dev":
        su_id = create_super_user().id
        db_init_setup(su_id)
    else:
        print("Production mod (need implementation)")


if __name__ == "__main__":
    main(SETTINGS_PATH)
