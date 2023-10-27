import uuid
from django.db import models, router

from ckeditor.fields import RichTextField
from autoslug import AutoSlugField


class ArticleQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        topic_id = kwargs.get("topic_id")
        alias = router.db_for_read(self.model, hints={"topic_id": topic_id})
        return models.QuerySet.get(self.using(alias), *args, **kwargs)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)


class Article(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic_id = models.PositiveSmallIntegerField(null=False)
    user_id = models.PositiveBigIntegerField(default=0)

    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        unique=True, 
        populate_from="title",
        unique_with=("topic_id", "title"),
    )
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    content = RichTextField()
    featured_image = models.ImageField(
        upload_to="articles/featured_images/%Y/%m/%d/",
        null=True,
    )

    objects = ArticleManager()

    def save(self, *args, **kwargs):
        hints = {"topic_id": self.topic_id}
        kwargs["using"] = router.db_for_write(self.__class__, hints=hints)
        super(Article, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        hints = {"topic_id": self.topic_id}
        kwargs["using"] = router.db_for_write(self.__class__, hints=hints)
        super(Article, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "Articles"
