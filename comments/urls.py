from django.urls import path
from comments.api.views import (
    CommentCreateApiView,
    CommentListApiView,
)


urlpatterns = [
	path('create/', CommentCreateApiView.as_view(), name='comment-create'),
	path('', CommentListApiView.as_view(), name='comment-list'),
]
