from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>', views.show_post, name='posts'),
    path('add/', views.add_post, name='add')
]