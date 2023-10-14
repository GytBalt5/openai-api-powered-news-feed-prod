from django.db import models, router

from ckeditor.fields import RichTextField
from autoslug import AutoSlugField

from news_feed.models import ArticleLastID


article_last_id_model = ArticleLastID()


class ArticleQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        uid = kwargs.get("uid")
        alias = router.db_for_read(self.model, hints={"uid": uid})
        return models.QuerySet.get(self.using(alias), *args, **kwargs)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)


class Article(models.Model):
    uid = models.PositiveBigIntegerField(null=True)

    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        unique=True,
        populate_from="title",
    )
    content = RichTextField()
    featured_image = models.ImageField(
        upload_to="articles/featured_images/%Y/%m/%d/",
        null=True,
    )
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    category_id = models.PositiveSmallIntegerField(null=True)
    user_id = models.PositiveBigIntegerField(null=True)

    objects = ArticleManager()

    def save(self, *args, **kwargs):
        if self.uid:  # an update operation
            hints = {"uid": self.uid}
        else:  # a new article creation operation
            uid = article_last_id_model.last_id + 1
            article_last_id_model.last_id = uid
            article_last_id_model.save()
            self.uid = uid

        hints = {"uid": self.uid}
        kwargs["using"] = router.db_for_write(self.__class__, hints=hints)
        super(Article, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        hints = {"uid": self.uid}
        kwargs["using"] = router.db_for_write(self.__class__, hints=hints)
        super(Article, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "Articles"
