import json
from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip
from rest_framework.test import APIClient
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer

class ArticleModelTestCase(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title='Test Article',
            body='This is a test article.',
            image='https://test-image.png'
            
        )

    def test_article_model(self):
        self.assertEqual(str(self.article), self.article.title)

class ArticleViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='tests')
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(
            title='Test Article',
            body='This is a test article.',
            image='https://test-image.png'
        )
        self.valid_payload = {
            "title": "Updated Test Article",
            "body": "This is an updated test article.",
            "image": "https://test-image.png"
        }
        self.invalid_payload = {
            'title': '',
            'body': 'This is an invalid test article.',
            'image': 45
        }

    def test_get_all_articles(self):
        response = self.client.get('/articles/')
        articles = Article.objects.all().order_by('created_at')
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(json.dumps(response.data['results']), json.dumps(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_article(self):
        response = self.client.post('/articles/?format=api', data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_article(self):
        response = self.client.post('/articles/', data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @skip("No implemented")
    def test_update_article(self):
        response = self.client.put('/articles/{}/'.format(self.article.id), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @skip("No implemented")
    def test_delete_article(self):
        response = self.client.delete('/articles/{}/'.format(self.article.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
