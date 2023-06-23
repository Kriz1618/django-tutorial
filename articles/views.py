from rest_framework import pagination, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

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
        return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def all_articles(self, request):
        """
        Returns a list of all articles
        """
        articles = Article.objects.all()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
