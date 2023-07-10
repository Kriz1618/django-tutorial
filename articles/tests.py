import json
from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip
from rest_framework.test import APIClient
from rest_framework import status
from .models import Article, Comment
from .serializers import ArticleSerializer


class ArticleModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='tests')
        self.article = Article.objects.create(
            title='Test Article',
            body='This is a test article.',
            image='https://test-image.png',
            author=self.user

        )

    def test_article_model(self):
        self.assertEqual(str(self.article), self.article.title)


class ArticleViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='tests')
        self.second_user = User.objects.create_user(
            username='second_user', password='tests')
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(
            title='Test Article', body='This is a test article.', image='https://test-image.png', author=self.user)
        self.article1 = Article.objects.create(
            title='Test Article 1', body='This is a test article 1.', image='https://test-image.png', author=self.user)
        self.article2 = Article.objects.create(
            title='Test Article 2', body='This is a test article 2', image='https://test-image.png', author=self.user)
        self.article3 = Article.objects.create(
            title='Test Article 3', body='This is a test article 3', image='https://test-image.png', author=self.user)
        self.valid_article_payload = {
            "title": "Updated Test Article",
            "body": "This is an updated test article.",
            "image": "https://test-image.png",
            "author": self.user
        }
        self.invalid_article_payload = {
            'title': '',
            'body': 'This is an invalid test article.',
            'image': 45
        }
        self.article1_comment = Comment.objects.create(
            article=self.article, title='Test comment', comment='Article', author=self.user)
        self.article1_comment1 = Comment.objects.create(
            article=self.article, title='Second comment', comment='Article 2', author=self.second_user)
        self.valid_comment_payload = {
            "title": "Article 1's comment",
            "comment": "Test comment"
        }
        self.invalid_comment_payload = {
            "title": "Article 1's comment",
            "comments": "Test comment"
        }

    def test_get_all_articles(self):
        response = self.client.get('/articles/')
        articles = Article.objects.all().order_by('created_at')
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(json.dumps(
            response.data['results']), json.dumps(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_articles_with_different_user(self):
        self.user = User.objects.create_user(
            username='user1', password='test')
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/articles/')
        self.assertEqual(json.dumps(
            response.data['results']), '[]')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_article(self):
        response = self.client.post(
            '/articles/?format=api', data=self.valid_article_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_article(self):
        response = self.client.post(
            '/articles/', data=self.invalid_article_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sorting_by_created_at_desc(self):
        response = self.client.get('/articles/?ordering=-created_at')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
        self.assertEqual(response.data['results'][0]['id'], self.article3.id)
        self.assertEqual(response.data['results'][1]['id'], self.article2.id)
        self.assertEqual(response.data['results'][2]['id'], self.article1.id)
        self.assertEqual(response.data['results'][3]['id'], self.article.id)

    def test_sorting_by_created_at_asc(self):
        response = self.client.get('/articles/?ordering=created_at')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
        self.assertEqual(response.data['results'][0]['id'], self.article.id)
        self.assertEqual(response.data['results'][1]['id'], self.article1.id)
        self.assertEqual(response.data['results'][2]['id'], self.article2.id)
        self.assertEqual(response.data['results'][3]['id'], self.article3.id)

    def test_pagination_with_page_size(self):
        response = self.client.get('/articles/?page_size=4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
        self.assertIn('next', response.data)
        self.assertIsNone(response.data['next'])

    def test_get_article_by_id(self):
        response = self.client.get(f'/articles/{self.article2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.article2.id)
        self.assertEqual(response.data['title'], self.article2.title)
        self.assertEqual(response.data['body'], self.article2.body)
        self.assertEqual(response.data['image'], self.article2.image)

    def test_update_article(self):
        response = self.client.put(
            '/articles/{}/'.format(self.article.id), data=self.valid_article_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_article(self):
        response = self.client.delete('/articles/{}/'.format(self.article.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_all_articles(self):
        url = '/articles/all_articles/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_valid_article_comment(self):
        response = self.client.post(
            f'/articles/{self.article.id}/comment/', data=self.valid_comment_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_article_comment(self):
        response = self.client.post(
            f'/articles/{self.article.id}/comment/', data=self.invalid_comment_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_article_comment(self):
        response = self.client.put(
            f'/comments/{self.article1_comment.id}/',
            data={ "title":"Updated comment", "comment": "new comment"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated comment')
        self.assertEqual(response.data['comment'], 'new comment')

    def test_get_articles_comments(self):
        response = self.client.get(f'/articles/{self.article.id}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_articles_comments_by_user(self):
        self.client.force_authenticate(user=self.second_user)
        response = self.client.get(f'/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.article1_comment1.title)

    def test_report_comment(self):
        response = self.client.post(f'/comments/{self.article1_comment1.id}/report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_count'], 1)

    def test_remove_comment_report(self):
        response = self.client.post(f'/comments/{self.article1_comment1.id}/report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_count'], 1)
        response = self.client.post(f'/comments/{self.article1_comment1.id}/remove_report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_count'], 0)

    def test_report_comment_allowed_times(self):
        self.usr1 = User.objects.create_user(username='usr1', password='tests')
        self.usr2 = User.objects.create_user(username='usr2', password='tests')
        self.usr3 = User.objects.create_user(username='usr3', password='tests')
        self.usr4 = User.objects.create_user(username='usr4', password='tests')
        self.usr5 = User.objects.create_user(username='usr5', password='tests')

        response = self.client.post(f'/comments/{self.article1_comment1.id}/report/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_count'], 1)
        self.client.force_authenticate(user=self.usr1)
        response = self.client.post(f'/comments/{self.article1_comment1.id}/report/')
        self.assertEqual(response.data['report_count'], 2)
        self.client.force_authenticate(user=self.usr2)
        response = self.client.post(f'/comments/{self.article1_comment1.id}/report/')
        self.assertEqual(response.data['report_count'], 3)
        self.client.force_authenticate(user=self.usr3)
        response = self.client.post(f'/comments/{self.article1_comment1.id}/report/')
        self.assertEqual(response.data['report_count'], 4)
        self.client.force_authenticate(user=self.usr4)
        response = self.client.post(f'/comments/{self.article1_comment1.id}/report/')
        self.assertEqual(response.data['report_count'], 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.usr5)
        response = self.client.post(f'/comments/{self.article1_comment1.id}/report/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
