from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'image',
                  'created_at', 'updated_at', 'is_public']


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(), required=False)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'article', 'title',
                  'user', 'comment', 'created_at', 'updated_at', 'reports')
        read_only_fields = ('id', 'reports')


class CommentReportSerializer(CommentSerializer):
    reported_by = UserSerializer(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'reported_by', 'reports')
