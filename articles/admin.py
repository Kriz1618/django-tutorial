from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "body", "image", "created_at")
    list_filter = ("title",)
    search_fields = ("title", "body")


admin.site.register(Article, ArticleAdmin)
