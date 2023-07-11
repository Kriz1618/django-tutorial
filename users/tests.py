from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class RegisterViewTestCase(TestCase):
    """Test module for RegisterView"""

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")

    def test_register_user(self):
        """Test API can create a user"""

        data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "test_pass",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "testuser@test.com")


class LoginViewTestCase(TestCase):
    """Test module for LoginView"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpass"
        )
        self.serializer_url = reverse("login")

    def test_login_user(self):
        """Test API can login a user"""

        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(self.serializer_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class LogoutViewTestCase(TestCase):
    """Test module for LogoutView"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        # self.serializer_url = reverse('logout')
        # self.token = self.get_access_token()

    def test_get_access_token(self):
        response = self.client.get("/api/protected/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post("/api/logout/", {"username": "testuser"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
