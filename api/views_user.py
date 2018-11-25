import json

from django.conf import settings

from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from api.models import AccountProfile
from api.models import Social
from api.models import FollowUser
from api.models import FollowStories

from api.serializers import UserSerializer
from api.serializers import AccountProfileSerializer
from api.serializers import AccountProfileCreateSerializer
from api.serializers import SocialSerializer
from api.serializers import SocialCreateSerializer
from api.serializers import UserEditSerializer
from api.serializers import FollowUserListSerializer
from api.serializers import FollowStoriesListSerializer

from api import custompermission


class UserListView(generics.ListAPIView):
    """
    List all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAdminUser,
    )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an user
    """
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        custompermission.IsUserOrReadonly,
    )


class AccountProfileListView(generics.RetrieveAPIView):
    """
    Retrieve a profile account
    """
    queryset = AccountProfile.objects.all()
    serializer_class = AccountProfileSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    lookup_field = ('user__username')



class AccountProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve and update a profile account
    """
    queryset = AccountProfile.objects.all()
    serializer_class = AccountProfileCreateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        custompermission.IsCurrentUserOrReadonly,
    )
    lookup_field = ('user__id')
    parser_classes = (MultiPartParser, FormParser, FileUploadParser,)




class SocialListView(generics.ListAPIView):
    """
    Retrieve a social account
    """
    serializer_class = SocialSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )

    def get_queryset(self):
        account = self.kwargs['account']
        return Social.objects.filter(account=account)


class SocialCreateView(generics.CreateAPIView):
    """
    Create a social account
    """
    serializer_class = SocialCreateSerializer
    pagination_class = None
    permission_classes = (
        permissions.IsAuthenticated,
    )


class FollowingUserListView(generics.ListAPIView):
    """
    Retrieve a profile account
    """
    queryset = FollowUser.objects.all()
    serializer_class = FollowUserListSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )

    def get_queryset(self):
        user = self.kwargs['user']
        return FollowUser.objects.filter(user_from__username=user)


class FollowingStoriesListView(generics.ListAPIView):
    """
    Retrieve a profile account
    """
    queryset = FollowStories.objects.all()
    serializer_class = FollowStoriesListSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )

    def get_queryset(self):
        user = self.kwargs['user']
        return FollowStories.objects.filter(from_user__username=user)
