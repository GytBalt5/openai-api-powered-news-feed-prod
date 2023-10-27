from articles.models import Article


def create_article(title, content, is_published, is_featured, topic_id, user_id):
    p = Article.objects.create(
        title=title,
        content=content,
        is_published=is_published,
        is_featured=is_featured,
        topic_id=topic_id,
        user_id=user_id,
    )
    return p
