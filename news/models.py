from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


class NewsPost(models.Model):
    title = models.CharField(max_length=64)
    text = RichTextUploadingField(blank=True, null=True)
    published = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ('post_without_moderation', "Can post without moderation")
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = RichTextUploadingField(blank=True, null=True)
    post = models.ForeignKey(
        NewsPost,
        on_delete=models.CASCADE,
        related_name='comments')
