import json

from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status, viewsets

from api.serializers import UserSerializer


class UserList(generics.ListAPIView):
    """
    List all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )


class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve an user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
