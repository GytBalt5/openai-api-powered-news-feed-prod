# Generated by Django 4.2.6 on 2023-10-26 22:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("news_feed", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ArticleLastID",
        ),
    ]
