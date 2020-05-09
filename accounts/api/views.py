from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from api import custompermission

from accounts.api.serializers import AccountProfileSerializer, FollowStoriesSerializer, FollowUserSerializer
from fanfics.api.serializers import UserFanficSerializer, SocialSerializer, UserSerializer

from accounts.models import AccountProfile, FollowUser, FollowStories, Social

class UserFanficDetailView(generics.RetrieveAPIView):
    """
    Retrieve an user formatted
    """
    queryset = User.objects.all()
    serializer_class = UserFanficSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = ('user__username')


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve an user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        custompermission.IsUserOrReadonly,
    )

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class AccountProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve and update a profile account
    """
    queryset = AccountProfile.objects.all()
    serializer_class = AccountProfileSerializer
    permission_classes = (
        permissions.AllowAny,
        custompermission.IsCurrentUserOrReadonly,
    )
    lookup_field = ('user__username')
    parser_classes = (MultiPartParser, FormParser, JSONParser,)




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
