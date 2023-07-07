# Generated by Django 4.2.2 on 2023-07-06 22:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0005_comment_reporters_comment_reports"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="reporters",
        ),
        migrations.AddField(
            model_name="comment",
            name="reported_by",
            field=models.ManyToManyField(
                related_name="reported_comments", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
