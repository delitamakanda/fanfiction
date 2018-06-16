import json
from django.shortcuts import render, HttpResponse
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
from api.serializers import FanficSerializer, FanficListSerializer
from api.serializers import ChapterSerializer
from api.serializers import CommentSerializer
from api.serializers import CommentCreateSerializer
from api.serializers import CategorySerializer
from api.serializers import SubCategorySerializer
from api.serializers import UserSerializer
from api.serializers import GenresSerializer
from api.serializers import ClassementSerializer
from api.serializers import StatusSerializer
from api import custompermission

"""
Liste des genres
"""
class GenresList(generics.ListAPIView):
    queryset = Fanfic.objects.all()[:1]
    serializer_class = GenresSerializer
    pagination_class = None
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='genre-list'


"""
Liste de classement
"""
class ClassementList(generics.ListAPIView):
    queryset = Fanfic.objects.all()[:1]
    serializer_class = ClassementSerializer
    pagination_class = None
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='classement-list'


"""
Liste des status
"""
class StatusList(generics.ListAPIView):
    queryset = Fanfic.objects.all()[:1]
    serializer_class = StatusSerializer
    pagination_class = None
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='status-list'


"""
Liste des news
"""
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = None
    name='post-list'


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='post-detail'


"""
Fanfics
"""

class FanficListByCategory(generics.ListAPIView):
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        custompermission.IsCurrentAuthorOrReadOnly,
    )
    name='fanfic-list-by-category'

    def get_queryset(self):
        category = self.kwargs['category']
        return Fanfic.objects.filter(category=category)


class FanficListBySubCategory(generics.ListAPIView):
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        custompermission.IsCurrentAuthorOrReadOnly,
    )
    name='fanfic-list-by-subcategory'

    def get_queryset(self):
        subcategory = self.kwargs['subcategory']
        return Fanfic.objects.filter(subcategory=subcategory)


class FanficListByAuthor(generics.ListAPIView):
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        custompermission.IsCurrentAuthorOrReadOnly,
    )
    name='fanfic-list-by-author'

    def get_queryset(self):
        user = self.kwargs['username']
        return Fanfic.objects.filter(author__username=user)


class FanficListRemastered(generics.ListAPIView):
    """
    Method GET ONLY
    """
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentAuthorOrReadOnly
    )
    name='fanfic-list-remastered'
    filter_fields = (
        'title',
        'publish',
    )
    search_fields = (
        '^title',
        '^description',
        '^credits',
        '^synopsis',
    )

    def get_queryset(self):
        return Fanfic.objects.all().filter(status='publié')


class FanficList(generics.ListCreateAPIView):
    """
    METHOD POST ONLY
    """
    serializer_class = FanficSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentAuthorOrReadOnly
    )
    name='fanfic-list'
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


class FanficListDetail(generics.RetrieveAPIView):
    throttle_scope = 'fanfic'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Fanfic.objects.all()
    serializer_class = FanficListSerializer
    name='fanfic-list-detail'
    # authentication_classes = (
        # TokenAuthentication,
    # )
    permission_classes = (
        # permissions.IsAuthenticated,
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentAuthorOrReadOnly,
    )


class ChapterList(generics.ListCreateAPIView):
    """
    Liste des chapitres
    """
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    name='chapter-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = None



class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    name='chapter-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class CommentList(generics.ListAPIView):
    """
    Liste des commentaires
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='comment-list'


class CommentListByFanfic(generics.ListAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='comment-list-by-fanfic'

    def get_queryset(self):
        fanfic = self.kwargs['fanfic']
        return Comment.objects.filter(fanfic=fanfic)


class CommentCreate(generics.CreateAPIView):
    """
    Create a comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-create'


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name='comment-detail'


class CategoryList(generics.ListCreateAPIView):
    """
    Liste des catégories
    """
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
    """
    Liste des sous-catégories
    """
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
    """
    List all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve an user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'fanfics' : reverse('fanfic-list', request=request),
            'fanfics-list-remastered': reverse('fanfic-list-remastered', request=request),
            'chapters': reverse('chapter-list', request=request),
            'comments': reverse('comment-list', request=request),
            'category': reverse('category-list', request=request),
            'sub-category': reverse('subcategory-list', request=request),
            'users': reverse('user-list', request=request),
            'posts' : reverse('post-list', request=request),
            'genres': reverse('genre-list', request=request),
            'status': reverse('status-list', request=request),
            'classements': reverse('classement-list', request=request),
        })
