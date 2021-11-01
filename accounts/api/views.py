from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from api import custompermission

from accounts.api.serializers import AccountProfileSerializer, FollowStoriesSerializer, FollowUserSerializer, SignupSerializer, GroupSerializer
from fanfics.api.serializers import UserFanficSerializer, SocialSerializer, FanficSerializer, UserSerializer

from accounts.models import AccountProfile, FollowUser, FollowStories, Social
from fanfics.models import Fanfic


class UserFanficDetailView(generics.RetrieveAPIView):
    """
    Retrieve an user formatted
    """
    queryset = User.objects.all()
    serializer_class = UserFanficSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = ('username')


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


class GroupListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
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
        """
        serializer = FollowUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        """
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


class FollowUserView(views.APIView):
    """
    Users followed
    """
    serializer_class = FollowUserSerializer()
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        return list of all authors followed
        """
        try:
            follow_users = FollowUser.objects.all()
            serializer = FollowUserSerializer(follow_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'no content'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer = FollowUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        follow_user_id = request.data.get('id')

        try:
            follow_user = FollowUser.objects.get(id=follow_user_id)
            follow_user.delete()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)


class FollowStoriesView(views.APIView):
    """
    Stories followed
    """
    serializer_class = FollowStoriesSerializer()
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        return list of all stories followed
        """
        try:
            stories = FollowStories.objects.all()
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
    authentication_classes = ()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
