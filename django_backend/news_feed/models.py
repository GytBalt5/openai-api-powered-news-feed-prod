from django.db import models

from autoslug import AutoSlugField

from core.utils import ARTICLES_DB_SHARDS

# TODO. Need to write a test for the create_article_shard function before implementing it.
# from utils.general import create_article_shard


class SingletonModel(models.Model):
    """
    An abstract base class model that representing a singleton instance.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save method for SingletonModel. Ensures that there's only one
        instance of the SingletonModel by setting the primary key to 1
        every time an object is saved.
        """
        self.pk = 1
        super().save(*args, **kwargs)


class Site(SingletonModel):
    """
    Model representing a singleton instance of the site's basic information.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="site/logo/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "site"
        verbose_name_plural = "site"


class Topic(models.Model):
    """
    Model representing a topic with a unique slug and description.
    Topics are used to categorize articles or content within the site.
    """

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        """
        Save method for Topic. If the topic is new, it triggers the creation
        of a new article shard before saving the topic.
        """

        # Temporary solution.
        shards_count = len(ARTICLES_DB_SHARDS)
        if Topic.objects.count() >= shards_count:
            raise Exception(f"Only {shards_count} topics can be created.")

        # Check if the object is new and doesn't have a primary key yet.
        # if not self.pk:
        #     create_article_shard()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics"
