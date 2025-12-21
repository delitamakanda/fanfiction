from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.http.response import Http404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (
	OutstandingToken,
	BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

from api import custompermission, custompagination

from accounts.api.serializers import AccountProfileSerializer, FollowStoriesSerializer, FollowUserSerializer, \
	SignupSerializer, GroupSerializer, UserFanficSerializer, SocialSerializer, UserSerializer, \
	DeleteProfilePhotoSerializer, ChangePasswordSerializer, SocialSignUpSerializer, NotificationSerializer, \
	ContentTypeSerializer, PasswordResetSerializer
from api.custompermission import IsAuthenticatedOrCreate

from fanfics.api.serializers import FanficSerializer
from accounts.models import AccountProfile, FollowUser, FollowStories, Social, Notification
from fanfics.models import Fanfic


class PasswordResetView(views.APIView):
	"""
	Allows users to reset their passwords.
	"""
	permission_classes = (permissions.AllowAny,)
	@staticmethod
	def post(request):
		serializer = PasswordResetSerializer(data=request.data)
		if serializer.is_valid():
			result = serializer.save()
			user = result['user']
			token = result['token']
			uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
			protocol = request.is_secure() and 'https' or 'http'
			link = f'{protocol}://{request.get_host()}/api/accounts/password_reset/{uidb64}/{token}/'
			send_mail(
				'Password reset request',
                f'To reset your password, visit this link: {link}',
                settings.EMAIL_HOST_USER,
                [user.email],
			)
			return Response({'message': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFanficDetailView(generics.RetrieveAPIView):
	"""
	Retrieve an user formatted
	"""
	queryset = User.objects.all()
	serializer_class = UserFanficSerializer
	lookup_field = 'username'
	permission_classes = (
		permissions.AllowAny,
	)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve an user
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	lookup_field = 'username'
	permission_classes = (
		custompermission.IsUserOrReadonly,
	)

	def put(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)


class AccountProfileDetailView(generics.RetrieveAPIView):
	"""
	Retrieve a profile account
	"""
	queryset = AccountProfile.objects.all()
	serializer_class = AccountProfileSerializer
	permission_classes = (
		permissions.AllowAny,
	)
	lookup_field = 'user__username'


class SocialListApiView(generics.ListCreateAPIView):
	"""
	Retrieve a social account
	"""
	serializer_class = SocialSerializer
	pagination_class = None
	permission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
	)

	def get_queryset(self):
		account = self.kwargs['account']
		if account:
			return Social.objects.filter(account=account)
		else:
			return Social.objects.all()


class SocialDestroyApiView(generics.DestroyAPIView):
	"""
	Destroy a social account
	"""
	queryset = Social.objects.all()
	serializer_class = SocialSerializer
	permission_classes = (
		permissions.IsAuthenticated,
	)


class GroupListView(generics.ListAPIView):
	permission_classes = [permissions.IsAuthenticated]
	required_scopes = ['groups']
	queryset = Group.objects.all()
	serializer_class = GroupSerializer


class SignupView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignupSerializer
	permission_classes = (custompermission.IsAuthenticatedOrCreate,)


def liked_fanfic(request):
	fanfic_id = request.data.get('id')
	user_id = request.data.get('user')

	if fanfic_id and user_id:
		try:
			fanfic = Fanfic.objects.get(id=int(fanfic_id))

			if fanfic:
				likes = fanfic.users_like.add(user_id)
				fanfic.users_like = likes
				fanfic.save()
			return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
		except:
			return Response({'status': 'nok'}, status=status.HTTP_400_BAD_REQUEST)


class FavoritedFanficView(views.APIView):
	"""
	Favorite fanfic
	"""
	# serializer_class = FanficSerializer()
	authentication_classes = ()
	permission_classes = ()

	def post(self, request, *args, **kwargs):
		serializer = FanficSerializer()
		if serializer.data:
			liked_fanfic(request)
		return Response(serializer.data, status=status.HTTP_200_OK)


def unliked_fanfic(request):
	fanfic_id = request.data.get('id')
	user_id = request.data.get('user')

	if fanfic_id and user_id:
		try:
			fanfic = Fanfic.objects.get(id=int(fanfic_id))

			if fanfic:
				likes = fanfic.users_like.remove(user_id)
				fanfic.users_like = likes
				fanfic.save()
			return Response({'status': 'ok'}, status=status.HTTP_200_OK)
		except:
			return Response({'status': 'nok'}, status=status.HTTP_400_BAD_REQUEST)


class UnfavoritedFanficView(views.APIView):
	"""
	Unfavorite fanfic
	"""
	serializer_class = FanficSerializer()
	authentication_classes = ()
	permission_classes = ()

	def post(self, request, *args, **kwargs):
		serializer = FanficSerializer()
		if serializer.data:
			unliked_fanfic(request)
		return Response(serializer.data, status=status.HTTP_200_OK)


class postFollowAuthor(generics.CreateAPIView):
	"""
	Follow an author
	"""
	serializer_class = FollowUserSerializer
	permission_classes = (permissions.IsAuthenticated,)


class unFollowAuthor(generics.DestroyAPIView):
	"""
	Unfollow an author
	"""
	serializer_class = FollowUserSerializer
	permission_classes = (permissions.IsAuthenticated,)
	lookup_field = 'user_from__username'


class FollowUserView(views.APIView):
	"""
	Users followed
	"""
	serializer_class = FollowUserSerializer
	pagination_class = custompagination.StandardResultsSetPagination
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)

	def get(self, request, username, format=None):
		"""
		return list of all authors followed
		"""
		try:
			follow_users = FollowUser.objects.filter(user_from__username=username)
			serializer = FollowUserSerializer(follow_users, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except:
			return Response({'status': 'no content'}, status=status.HTTP_204_NO_CONTENT)


	def delete(self, request, pk=None):
		follow_user_id = request.data.get('id')

		try:
			follow_user = FollowUser.objects.get(id=follow_user_id)
			follow_user.delete()
			return Response({'status': 'ok'}, status=status.HTTP_200_OK)
		except:
			return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)

class FollowAuthorDeleteView(views.APIView):
	"""
	Author followed
	"""
	serializer_class = FollowUserSerializer()
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)

	def get_object(self, request, user_to):
		user_from = request.data.get('user_from')
		try:
			return FollowUser.objects.get(user_to=user_to, user_from=user_from)
		except FollowUser.DoesNotExist:
			raise Http404

	def get(self, request, user_to, format=None):
		author_followed = self.get_object(request, user_to)
		serializer = FollowUserSerializer(author_followed)
		return Response(serializer.data)

	def delete(self, request, user_to, format=None):
		author_followed = self.get_object(request, user_to)
		author_followed.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class FollowStoriesDeleteView(views.APIView):
	"""
	Author followed
	"""
	serializer_class = FollowStoriesSerializer()
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)

	def get_object(self, request, to_fanfic):
		from_user = request.data.get('from_user')
		try:
			return FollowStories.objects.get(to_fanfic=to_fanfic, from_user=from_user)
		except FollowStories.DoesNotExist:
			raise Http404

	def get(self, request, to_fanfic, format=None):
		story_followed = self.get_object(request, to_fanfic)
		serializer = FollowStoriesSerializer(story_followed)
		return Response(serializer.data)

	def delete(self, request, to_fanfic, format=None):
		story_followed = self.get_object(request, to_fanfic)
		story_followed.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class FollowStoriesView(views.APIView):
	"""
	Stories followed
	"""
	serializer_class = FollowStoriesSerializer
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)

	def get(self, request, username, format=None):
		"""
		return list of all stories followed
		"""
		try:
			stories = FollowStories.objects.filter(from_user__username=username)
			serializer = FollowStoriesSerializer(stories, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except:
			return Response({'status': 'no content'}, status=status.HTTP_204_NO_CONTENT)

	def post(self, request):
		serializer = FollowStoriesSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk=None):
		follow_story_id = request.data.get('id')

		try:
			follow_story = FollowStories.objects.get(id=follow_story_id)
			follow_story.delete()
			return Response({'status': 'ok'}, status=status.HTTP_200_OK)
		except:
			return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(views.APIView):
	"""
	Disable user account
	"""
	serializer_class = UserSerializer()

	def get(self, request, *args, **kwargs):
		user = request.user
		user.is_active = False
		user.save()
		return Response({"status": "ok"}, status=status.HTTP_200_OK)

class SocialSignUp(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SocialSignUpSerializer
	permission_classes = (IsAuthenticatedOrCreate,)

	def create(self, request, *args, **kwargs):
		pass



class UserCreateView(generics.CreateAPIView):
	"""
	Create an user
	"""
	serializer_class = UserSerializer
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)


class LoginView(views.APIView):
	"""
	Login user
	"""
	serializer_class = UserSerializer
	permission_classes = (permissions.AllowAny,)

	@staticmethod
	def post(request):
		user = authenticate(
			username=request.data.get("username"),
			password=request.data.get("password"))

		if user is None or not user.is_active:
			return Response({
				'status': 'Non autorisé',
				'message': 'Pseudo ou mot de passe incorrect.'
			}, status=status.HTTP_401_UNAUTHORIZED)

		request.session.set_expiry(7200)
		login(request, user)
		return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
	"""
	Logout user
	"""
	permissions_classes = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		if self.request.data.get("all"):
			token: OutstandingToken
			for token in OutstandingToken.objects.filter(user=request.user):
				_, _ = BlacklistedToken.objects.get_or_create(token=token)
			return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
		refresh_token = self.request.data.get("refresh_token")
		token = OutstandingToken(token=refresh_token)
		token.save()
		return Response({"status": 204})


class CheckoutUserView(views.APIView):
	"""
	Checkout current user
	"""
	serializer_class = UserSerializer

	@staticmethod
	def get(request):
		serializer = UserSerializer(request.user)
		return Response(serializer.data, status=status.HTTP_200_OK)



class ChangePasswordView(views.APIView):
	"""
	Change password view
	"""
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = ChangePasswordSerializer

	def get_object(self, queryset=None):
		return self.request.user

	def put(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = ChangePasswordSerializer(data=request.data)

		if serializer.is_valid():
			old_password = serializer.data.get('old_password')
			if not self.object.check_password(old_password):
				return Response({'old_password': ['Mot de passe erroné.']}, status=status.HTTP_400_BAD_REQUEST)
			self.object.set_password(serializer.data.get('new_password'))
			self.object.save()
			return Response(status=status.HTTP_204_NO_CONTENT)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemovePhotoFromAccount(views.APIView):
	"""
	Photo Profile
	"""
	permission_classes = (permissions.IsAuthenticated,)

	@staticmethod
	def get_object(pk):
		try:
			return AccountProfile.objects.get(pk=pk)
		except AccountProfile.DoesNotExist:
			raise Http404

	def put(self, request, pk):
		photo = self.get_object(pk)
		serializer = DeleteProfilePhotoSerializer(photo, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactMailView(views.APIView):
	"""
	Send an email to webmaster
	"""
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()

	@staticmethod
	def post(request, *args, **kwargs):
		from_email = request.data.get('from_email')
		subject = request.data.get('subject')
		message = request.data.get('message')

		if subject and message and from_email:
			try:
				send_mail(subject, message, from_email,
						  [settings.SERVER_EMAIL])
			except BadHeaderError:
				return Response({"status": "invalid headers"}, status=status.HTTP_400_BAD_REQUEST)
			return Response({"status": "ok"}, status=status.HTTP_200_OK)
		else:
			return Response({"status": "nok"}, status=status.HTTP_400_BAD_REQUEST)


"""
Notification generics views
"""


class ContentTypeView(generics.RetrieveAPIView):
	queryset = ContentType.objects.all()
	serializer_class = ContentTypeSerializer
	permission_classes = (
		permissions.IsAuthenticated,
	)


class NotificationListView(generics.ListAPIView):
	queryset = Notification.objects.all()
	serializer_class = NotificationSerializer
	permission_classes = (
		permissions.IsAuthenticated,
	)

	def get_queryset(self):
		notifications = Notification.objects.exclude(user=self.request.user)
		following_ids = self.request.user.following.values_list(
			'id', flat=True)

		if following_ids:
			notifications = notifications.filter(user_id__in=following_ids).select_related(
				'user', 'user__accountprofile').prefetch_related('target')

		notifications = notifications[:20]

		return notifications
