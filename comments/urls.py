from django.urls import path
from comments.api.views import (
    CommentCreateApiView,
    CommentListApiView,
CommentUpdateApiView,
)

app_name = 'comments'

urlpatterns = [
	path('create/', CommentCreateApiView.as_view(), name='comment-create'),
	path('<int:pk>/update/', CommentUpdateApiView.as_view(), name='comment-update'),
	path('', CommentListApiView.as_view(), name='comment-list'),
]
