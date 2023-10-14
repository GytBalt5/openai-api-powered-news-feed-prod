from django.contrib import admin
from django.contrib.auth import get_user_model

from news_feed.models import Category, Site
from articles.models import Article


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "date_joined")


class CategoryAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "is_featured", "created_at")


admin.site.register(Site)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
