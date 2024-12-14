from rest_framework import generics, permissions

from comments.models import Comment

from comments.api.serializers import CommentSerializer, CommentCreateSerializer
from api.custompermission import IsCurrentSessionOrReadOnly


class CommentCreateApiView(generics.CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateSerializer
	permission_classes = (
		permissions.IsAuthenticated,
	)
	name='comment-create'

	def perform_create(self, serializer):
			self.request.session['comment_session_id'] = serializer.validated_data['chapter'].id


class CommentUpdateApiView(generics.UpdateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateSerializer
	permission_classes = (
		IsCurrentSessionOrReadOnly,
	)
	lookup_field = 'id'
	lookup_url_kwarg = 'id'
	name='comment-update'


class CommentListApiView(generics.ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = (
		permissions.AllowAny,
	)
	filter_fields = (
		'fanfic',
		'chapter',
		'active',
	)
	ordering_fields = (
		'-created',
	)
	name='comment-list'
