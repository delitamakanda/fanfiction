from django.urls import path
from posts import views

from posts.api.views import (
    PostCreateAPIView,
    PostDetailAPIView,
    PostListAPIView,
    PostUpdateAPIView,
    TagListAPIView,
)

urlpatterns = [
    path('list/', views.PostsListView.as_view(), name='list-posts'),
    path('fake/', views.generate_fake_data, name='generate_fake_data'),
path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('', PostListAPIView.as_view(), name='post-list'),
    path('create/', PostCreateAPIView.as_view(), name='post-create'),
    path('<int:pk>/update/',
         PostUpdateAPIView.as_view(), name='post-update'),
    path('<int:pk>/remove/',
         PostUpdateAPIView.as_view(), name='post-delete'),
    path('<str:slug>/', PostDetailAPIView.as_view(), name='post-detail'),
]
