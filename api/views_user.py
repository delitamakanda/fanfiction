import json

from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status, viewsets

from api.models import AccountProfile

from api.serializers import UserSerializer
from api.serializers import AccountProfileSerializer

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
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        custompermission.IsCurrentUserOrReadonly,
    )


class AccountProfileListView(generics.RetrieveAPIView):
    """
    Retrieve a profile account
    """
    queryset = AccountProfile.objects.all()
    serializer_class = AccountProfileSerializer
    permissions_classes = (
        permissions.AllowAny,
    )

    lookup_field = ('user__username')
