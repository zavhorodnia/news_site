from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.index, name='index'),
    path('posts/to_moderate/', views.waiting_for_moderation, name='waiting_for_moderation'),
    path('posts/<int:post_id>', views.show_post, name='posts'),
    path('posts/add/', views.add_post, name='add'),
    path('posts/<int:post_id>/moderate', views.moderate_post, name='moderate'),
    path('posts/<int:post_id>/send_to_moderation', views.send_to_moderation, name='send_to_moderation'),
    path('posts/<int:post_id>/publish', views.publish, name='publish'),
    path('posts/<int:post_id>/comments/<int:comment_id>', views.delete_comment, name='delete_comment')
]