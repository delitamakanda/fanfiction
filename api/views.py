import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from rest_framework.throttling import ScopedRateThrottle
from api.models import Fanfic
from api.models import Comment
from api.models import Chapter
from api.models import Category
from api.models import SubCategory
from api.models import Post
from api.serializers import PostSerializer
from api.serializers import FanficSerializer
from api.serializers import ChapterSerializer
from api.serializers import CommentSerializer
from api.serializers import CategorySerializer
from api.serializers import SubCategorySerializer
from api.serializers import UserSerializer
from api.serializers import OptionsSerializer
from api import custompermission

# Create your views here.
class OptionsList(viewsets.ModelViewSet):
    queryset = Fanfic.objects.all()[:1]
    serializer_class = OptionsSerializer
    pagination_class = None
    permission_feclasses = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='options-list'


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='post-list'


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='post-detail'


class FanficListByAuthor(generics.ListAPIView):
    serializer_class = FanficSerializer
    pagination_class = None
    permission_classes = (
        custompermission.IsCurrentAuthorOrReadOnly,
    )

    def get_queryset(self):
        # queryset = Fanfic.objects.all()
        # username = self.request.query_params.get('username', None)
        # if username is not None:
        #     queryset = queryset.filter(author__username=username)
        # return queryset
        user = self.kwargs['username']
        return Fanfic.objects.filter(author__username=user)



class FanficList(generics.ListCreateAPIView):
    serializer_class = FanficSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentAuthorOrReadOnly
    )
    # authentication_classes = (
        # TokenAuthentication,
    # )
    # permission_classes = (
        # permissions.IsAuthenticated,
    # )
    name='fanfic-list'
    filter_fields = (
        'title',
        'genres',
        'category',
        'subcategory',
    )
    search_fields = (
        '^title',
    )
    ordering_fields = (
        'title',
        'publish',
    )
    pagination_class = None

    def get_queryset(self):
        return Fanfic.objects.all().filter(status='publié')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class FanficDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_scope = 'fanfic'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Fanfic.objects.all()
    serializer_class = FanficSerializer
    name='fanfic-detail'
    # authentication_classes = (
        # TokenAuthentication,
    # )
    permission_classes = (
        # permissions.IsAuthenticated,
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentAuthorOrReadOnly,
    )
    pagination_class = None


class ChapterList(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    name='chapter-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = None


# class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Fanfic.objects.all()
    # serializer_class = ChapterSerializer
    # name='chapter-detail'


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='comment-list'


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='comment-detail'


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='category-list'
    filter_fields = (
        'name',
    )
    search_fields = (
        '^name',
    )
    ordering_fields = (
        'name',
    )
    pagination_class = None


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='category-detail'


class SubCategoryList(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='subcategory-list'
    pagination_class = None


class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='subcategory-detail'


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    """
    Create an user
    """
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()


class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve an user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(views.APIView):
    """
    Login user
    """
    serializer_class = UserSerializer
    permission_classes = ( permissions.AllowAny,)

    def post(self, request):
        user = authenticate (
            username=request.data.get("username"),
            password=request.data.get("password"))

        if user is None or not user.is_active:
            return Response({
                'status': 'Non autorisé',
                'message': 'Pseudo ou mot de passe incorrect.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response(UserSerializer(user).data)

    # def post(self, request, *args, **kwargs):
    #     login(request, request.user)
    #     return Response(UserSerializer(request.user).data)

class LogoutView(views.APIView):
    """
    Logout user
    """
    permission_classes = ( permissions.AllowAny,)

    def get(self, request):
        logout(request)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class CheckoutUserView(views.APIView):
    """
    Checkout current user
    """
    serializer_class = UserSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        if request.user:
            return Response(serializer.data, status=status.HTTP_200_OK)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'fanfics' : reverse('fanfic-list', request=request),
            'chapters': reverse('chapter-list', request=request),
            'comments': reverse('comment-list', request=request),
            'category': reverse('category-list', request=request),
            'sub-category': reverse('subcategory-list', request=request),
            'users': reverse('user-list', request=request),
            'posts' : reverse('post-list', request=request),
            'options': reverse('option-list', request=request),
        })
