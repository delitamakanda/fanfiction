from django.urls import path

from posts.api import views as views_post

urlpatterns = [
    path('tags', views_post.TagList.as_view(), name='tag-list'),
    path('posts', views_post.PostList.as_view(), name='post-list'),
    path('posts/create', views_post.PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/edit', views_post.PostUpdate.as_view(), name='post-update'),
    path('posts/<str:slug>', views_post.PostDetail.as_view(), name='post-detail'),
]