from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login, name='login'),
    path('', views.index, name='index'),
    path('posts/<int:post_id>', views.show_post, name='posts'),
    path('posts/add/', views.add_post, name='add')
]