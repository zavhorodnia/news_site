from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .tokens import account_activation_token


@shared_task
def notify_on_comment(current_site, post, comment_author):
    send_mail(
        'New comment on your post',
        render_to_string('news/comment_notification_email.html', {
            'post': post,
            'username': post.author.username,
            'domain': current_site.domain,
            'comment_author': comment_author,
        }),
        'noreply@example.com',
        [post.author.email],
        fail_silently=False
    )


@shared_task
def send_confirmation_mail(user, domain):
    try:
        return send_mail(
            'Confirm your email',
            render_to_string('news/confirm_email.html', {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }),
            'noreply@example.com',
            [user.email],
            fail_silently=False
        )
    except:
        return False
