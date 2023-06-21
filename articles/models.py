from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.URLField(max_length=200)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
