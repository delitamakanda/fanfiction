import json

from django.shortcuts import render, HttpResponse
from django.http import Http404, HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from social_django.utils import load_strategy
from social_django.utils import load_backend
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import AuthAlreadyAssociated

from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.response import Response

from api.serializers import ChangePasswordSerializer
from api.serializers import UserSerializer
from accounts.api.serializers import DeleteProfilePhotoSerializer, SocialSignUpSerializer

from accounts.models import AccountProfile

from api.custompermission import IsAuthenticatedOrCreate


class SocialSignUp(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SocialSignUpSerializer
	permission_classes = (IsAuthenticatedOrCreate,)

	def create(self, request, *args, **kwargs):
		"""
		Override `create` instead of `perform_create` to access request
		request is necessary for `load_strategy`
		"""
		# https://yeti.co/blog/social-auth-with-django-rest-framework/
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		provider = request.data['provider']

		# If this request was made with an authenticated user, try to associate this social
		# account with it
		authed_user = request.user if not request.user.is_anonymous() else None

		# `strategy` is a python-social-auth concept referencing the Python framework to
		# be used (Django, Flask, etc.). By passing `request` to `load_strategy`, PSA
		# knows to use the Django strategy
		strategy = load_strategy(request)
		# Now we get the backend that corresponds to our user's social auth provider
		# e.g., Facebook, Twitter, etc.
		backend = load_backend(
			strategy=strategy, name=provider, redirect_uri=None)

		if isinstance(backend, BaseOAuth1):
			# Twitter, for example, uses OAuth1 and requires that you also pass
			# an `oauth_token_secret` with your authentication request
			token = {
				'oauth_token': request.data['access_token'],
				'oauth_token_secret': request.data['access_token_secret'],
			}
		elif isinstance(backend, BaseOAuth2):
			# We're using oauth's implicit grant type (usually used for web and mobile
			# applications), so all we have to pass here is an access_token
			token = request.data['access_token']

		try:
			# if `authed_user` is None, python-social-auth will make a new user,
			# else this social account will be associated with the user you pass in
			user = backend.do_auth(token, user=authed_user)
		except AuthAlreadyAssociated:
			# You can't associate a social account with more than user
			return Response({"errors": "That social media account is already in use"},
							status=status.HTTP_400_BAD_REQUEST)

		if user and user.is_active:
			# if the access token was set to an empty string, then save the access token
			# from the request
			auth_created = user.social_auth.get(provider=provider)
			if not auth_created.extra_data['access_token']:
				# Facebook for example will return the access_token in its response to you.
				# This access_token is then saved for your future use. However, others
				# e.g., Instagram do not respond with the access_token that you just
				# provided. We save it here so it can be used to make subsequent calls.
				auth_created.extra_data['access_token'] = token
				auth_created.save()

			# Set instance since we are not calling `serializer.save()`
			serializer.instance = user
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED,
							headers=headers)
		else:
			return Response({"errors": "Error with social authentication"},
							status=status.HTTP_400_BAD_REQUEST)


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

	def post(self, request):
		# profile = AccountProfile.objects.all()

		user = authenticate(
			username=request.data.get("username"),
			password=request.data.get("password"))

		if user is None or not user.is_active:
			return Response({
				'status': 'Non autorisé',
				'message': 'Pseudo ou mot de passe incorrect.'
			}, status=status.HTTP_401_UNAUTHORIZED)

		# if not profile.filter(user=user).exists():
			# AccountProfile.objects.create(user=user)

		request.session.set_expiry(7200)
		login(request, user)
		return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
	"""
	Logout user
	"""
	permissions_classes = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		if self.request.data.get('all'):
			token: OutstandingToken
			for token in OutstandingToken.objects.filter(user=request.user):
				_, _ = BlacklistedToken.objects.get_or_create(token=token)
			return Response({"status": "ok"}, status=status.HTTP_200_OK)
		refresh_token = self.request.data.get('refresh_token')
		token = RefreshToken(token=refresh_token)
		token.blacklist()
		return Response({"status": "ok"}, status=status.HTTP_204_NO_CONTENT)


class CheckoutUserView(views.APIView):
	"""
	Checkout current user
	"""
	serializer_class = UserSerializer

	def get(self, request):
		print(request.user)
		serializer = UserSerializer(request.user)
		if request.user:
			return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(views.APIView):
	"""
	Change password view
	"""
	permission_classes = (permissions.IsAuthenticated,)

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

	def get_object(self, pk):
		try:
			return AccountProfile.objects.get(pk=pk)
		except AccountProfile.DoesNotExist:
			raise Http404

	def put(self, request, pk, format=None):
		photo = self.get_object(pk)
		serializer = DeleteProfilePhotoSerializer(photo, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
