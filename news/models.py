from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


class NewsPost(models.Model):
    title = models.CharField(max_length=64)
    text = RichTextUploadingField(blank=True, null=True)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = [
            ('post_without_moderation', "Can post without moderation")
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(help_text='What do you think about it?', max_length=1024)
    post = models.ForeignKey(
        NewsPost,
        on_delete=models.CASCADE,
        related_name='comments')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
