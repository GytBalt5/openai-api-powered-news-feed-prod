from django.db import models

from autoslug import AutoSlugField


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # ensure instance can't be deleted


# General information for the entire website.
class Site(SingletonModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="site/logo/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "site"
        verbose_name_plural = "Site"


class ArticleLastID(SingletonModel):
    last_id = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return str(self.last_id)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "Categories"
