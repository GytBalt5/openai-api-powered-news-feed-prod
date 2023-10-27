from django.db import models

from autoslug import AutoSlugField

from core.utils import ARTICLES_DB_SHARDS


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # ensure instance can't be deleted


class Site(SingletonModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="site/logo/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "site"
        verbose_name_plural = "Site"


class Category(models.Model):
    """
    TODO. 
    1. Need to rename the Category to the Topic.
    2. Need to generate new databases (shards) for articles dynamically 
    when a new category is created.
    """

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        """
        Temporary solution to limit the number of categories 
        to the static number of article shards.
        """
        shards_count = len(ARTICLES_DB_SHARDS)
        if Category.objects.count() >= shards_count:
            raise Exception(f"Only {shards_count} topics can be created.")
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "Categories"
