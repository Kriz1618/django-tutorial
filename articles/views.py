from rest_framework import viewsets
from rest_framework import permissions

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('created_at')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.query_params.get('sort', None)
        page_size = self.request.query_params.get('page_size', None)
        if sort == 'asc':
            queryset = queryset.order_by('created_at')
        elif sort == 'desc':
            queryset = queryset.order_by('-created_at')
        if page_size is not None:
            self.pagination_class.page_size = int(page_size)
        return queryset
