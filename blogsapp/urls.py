
from django.urls import path

from . import views

urlpatterns = [
    path('post/', views.posts_list, name='posts_list'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('post/write', views.post_write, name='post_write'),
]