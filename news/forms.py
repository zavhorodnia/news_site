from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import NewsPost, Comment


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=16, help_text='Required')
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign up'))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=16, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Log in'))


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'text']


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Comment'))