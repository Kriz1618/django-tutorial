from .models import Article, Comment
from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'image', 'created_at', 'updated_at', 'is_public']


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(), required=False)
    article_title = serializers.CharField(
        source='article.title', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'article', 'article_title', 'title',
                  'user', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at')

