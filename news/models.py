from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class NewsPost(models.Model):
    title = models.CharField(max_length=64)
    text = RichTextField()
    accepted = models.BooleanField()
    # author = models.ForeignKey(User)

    class Meta:
        permissions = [
            ('post_without_moderation', "Can post without moderation")
        ]


class Comment(models.Model):
    text = RichTextField()
    post = models.ForeignKey(
        NewsPost,
        on_delete=models.CASCADE,
        related_name='comments')
