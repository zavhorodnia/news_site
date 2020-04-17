from django.shortcuts import render, get_object_or_404
from .models import NewsPost
from .forms import NewsPostForm


def index(request):
    context = {
        'posts': NewsPost.objects.filter(accepted=True)[:5],
        'can_moderate': request.user.has_perm('post_without_moderation')
    }
    return render(request, 'news/index.html', context)


def show_post(request, post_id):
    context = {'post': get_object_or_404(NewsPost.objects.get(id=post_id))}
    return render(request, 'news/post.html', context)


def add_post(request):
    context = {
        'post_form': NewsPostForm(),
        'can_post': request.user.has_perm('post_without_moderation')
    }
    return render(request, 'news/add_post.html', context)
