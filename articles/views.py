from rest_framework import viewsets, pagination
from rest_framework import permissions

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
    ordering_fields = ('created_at', '-created_at')

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering', None)
        if ordering and ordering in self.ordering_fields:
            queryset = queryset.order_by(ordering)
        return queryset
