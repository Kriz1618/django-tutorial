from rest_framework import pagination, permissions, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework import permissions
from django.core.exceptions import PermissionDenied

from .models import Article
from .serializers import ArticleSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('created_at')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['title', 'created_at']

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(author=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.author != self.request.user:
            raise PermissionDenied(
                'You don\'t have permission to modify this article.')

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'You don\'t have permission to delete this article.')
        instance.delete()
