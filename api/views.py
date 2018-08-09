import json
from django.shortcuts import render, HttpResponse
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
from api.models import FlatPages
from api.serializers import ChapterSerializer
from api.serializers import CommentSerializer
from api.serializers import CommentCreateSerializer
from api.serializers import CategorySerializer
from api.serializers import SubCategorySerializer
from api.serializers import GenresSerializer
from api.serializers import ClassementSerializer
from api.serializers import StatusSerializer
from api.serializers import FlatPagesSerializer
from api import custompermission

"""
Liste des genres
"""
class GenresList(generics.ListAPIView):
    queryset = Fanfic.objects.all()[:1]
    serializer_class = GenresSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
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
        permissions.AllowAny,
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
        permissions.AllowAny,
    )
    name='status-list'


"""
FlatPages
"""

class FlatPagesView(generics.ListAPIView):
    serializer_class = FlatPagesSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name = 'pages'

    """docstring for FlatPagesView."""
    def get_queryset(self):
        type = self.kwargs['type']
        if type:
          return FlatPages.objects.filter(type=type)
        else:
          return FlatPages.objects.all()


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
