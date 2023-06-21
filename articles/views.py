from rest_framework import pagination, permissions, viewsets
from rest_framework.filters import OrderingFilter

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
    ordering_fields = ['title','created_at']
