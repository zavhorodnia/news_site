from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import NewsPost
from .forms import NewsPostForm


@login_required(login_url='/login/')
def index(request):
    context = {
        'posts': NewsPost.objects.all(), #filter(published=True),
        'can_moderate': request.user.has_perm('post_without_moderation')
    }
    return render(request, 'news/index.html', context)


@login_required(login_url='/login/')
def show_post(request, post_id):
    context = {'post': get_object_or_404(NewsPost.objects.get(id=post_id))}
    return render(request, 'news/post.html', context)


@login_required(login_url='/login/')
def add_post(request):
    if request.method == 'POST':
        form = NewsPostForm(request.POST)
        context = {
            'post_form': form,
            'can_post': request.user.has_perm('post_without_moderation')
        }
        if form.is_valid():
            post_item = form.save()
            if request.user.has_perm('post_without_moderation'):
                post_item.published = True
            post_item.save()
            return redirect('/')
    else:
        form = NewsPostForm()
        context = {'post_form': form}
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
                login(user)
                return redirect('')
            else:
                context = {'form': form, 'invalid': True}
    else:
        context = {'form': LoginForm()}
    return render(request, 'news/login.html', context)


@login_required(login_url='/login/')
def logout(request):
    django_logout(request)
    return redirect('login/')


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
            except:
                user.delete()
                return HttpResponse(
                    'Something went wrong. Check your email or contact administrator',
                    status=400)
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
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can log in to your account.')
    else:
        return HttpResponse('Activation link is invalid!')
