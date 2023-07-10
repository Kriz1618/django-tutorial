from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    reports = models.IntegerField(default=0)
    reported_by = models.ManyToManyField(User, related_name='reported_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def report(self, user):
        if user not in self.reported_by.all():
            self.reported_by.add(user)
            self.reports += 1
            self.save()
        return self.reported_by.count()

    def remove_report(self, user):
        if user in self.reported_by.all():
            self.reported_by.remove(user)
            self.reports -= 1
            self.save()            
        return self.reported_by.count()
