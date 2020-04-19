from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import NewsPost, Comment
from .forms import NewsPostForm, CommentPostForm


@login_required(login_url='/login/')
def index(request):
    context = {
        'posts': NewsPost.objects.filter(published=True).order_by('-id'),
        'is_moderator': request.user.has_perm('post_without_moderation')
    }
    return render(request, 'news/index.html', context)


@login_required(login_url='/login/')
def waiting_for_moderation(request):
    if not request.user.has_perm('post_without_moderation'):
        return redirect('index')
    context = {'posts': NewsPost.objects.filter(published=False).order_by('-id'),
               'is_moderator': True}
    return render(request, 'news/waiting_for_moderation.html', context)


@login_required(login_url='/login/')
def show_post(request, post_id):
    if request.method == 'POST':
        form = CommentPostForm(request.POST)
        post = NewsPost.objects.get(id=post_id)
        if form.is_valid():
            comment_item = form.save(commit=False)
            comment_item.author = request.user
            comment_item.post = post
            comment_item.save()
            notify_on_comment(get_current_site(request), post, request.user)
    else:
        try:
            post = NewsPost.objects.get(id=post_id)
        except NewsPost.DoesNotExist:
            return redirect('index')
    context = {
        'post': post,
        'is_moderator': request.user.has_perm('post_without_moderation'),
        'comments': post.comments.all().order_by('-id'),
        'form': CommentPostForm()}
    return render(request, 'news/post.html', context)


@login_required(login_url='/login/')
def add_post(request):
    if request.method == 'POST':
        form = NewsPostForm(request.POST)
        context = {
            'post_form': form,
        }
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.author = request.user
            if request.user.has_perm('post_without_moderation'):
                post_item.published = True
            post_item.save()
            return redirect('/')
    else:
        context = {
            'post_form': NewsPostForm(),
            'is_moderator': request.user.has_perm('post_without_moderation')
        }
    return render(request, 'news/add_post.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                return redirect('index')
            else:
                context = {'form': form, 'invalid': True}
    else:
        context = {'form': LoginForm()}
    return render(request, 'news/login.html', context)


@login_required(login_url='/login/')
def logout(request):
    django_logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            try:
                send_mail(
                    'Confirm your email',
                    render_to_string('news/confirm_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }),
                    'zavhorodnia.yevheniia@gmail.com',
                    [form.cleaned_data.get('email')],
                    fail_silently=False
                )
                print(form.cleaned_data.get('email'))
            except:
                user.delete()
                return render(request, 'news/confirmation_failed.html')
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'news/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        django_login(request, user)
        return render(request, 'news/confirmation_successfull.html')
    else:
        return HttpResponse('Activation link is invalid!')


def notify_on_comment(current_site, post, comment_author):
    send_mail(
        'New comment on your post',
        render_to_string('news/comment_notification_email.html', {
            'post': post,
            'username': post.author.username,
            'domain': current_site.domain,
            'comment_author': comment_author,
        }),
        'zavhorodnia.yevheniia@gmail.com',
        [post.author.email],
        fail_silently=False
    )


@login_required(login_url='/login/')
def moderate_post(request, post_id):
    if not request.user.has_perm('post_without_moderation'):
        return redirect('index')
    try:
        post = NewsPost.objects.get(id=post_id)
    except NewsPost.DoesNotExist:
        return redirect('index')
    if request.method == 'POST':
        form = NewsPostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.save()
            return redirect('waiting_for_moderation')
    else:
        form = NewsPostForm(instance=post)
        return render(request, 'news/moderate_post.html', {'form': form})


@login_required(login_url='/login/')
def send_to_moderation(request, post_id):
    try:
        post = NewsPost.objects.get(id=post_id)
        if request.user.has_perm('post_without_moderation'):
            post.published = False
            post.save()
    except NewsPost.DoesNotExist:
        pass
    finally:
        return redirect('index')


@login_required(login_url='/login/')
def publish(request, post_id):
    try:
        post = NewsPost.objects.get(id=post_id)
        if request.user.has_perm('post_without_moderation'):
            post.published = True
            post.save()
    except NewsPost.DoesNotExist:
        pass
    finally:
        return redirect('waiting_for_moderation')


@login_required(login_url='/login/')
def delete_comment(request, post_id, comment_id):
    try:
        NewsPost.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        if request.user.has_perm('post_without_moderation'):
            comment.delete()
    except (NewsPost.DoesNotExist, Comment.DoesNotExist):
        pass
    finally:
        return redirect('posts', post_id=post_id)
