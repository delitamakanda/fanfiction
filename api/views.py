from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.models import Fanfic
from api.models import Comment
from api.models import Chapter
from api.models import Category
from api.models import SubCategory
from api.serializers import FanficSerializer
from api.serializers import ChapterSerializer
from api.serializers import CommentSerializer
from api.serializers import CategorySerializer
from api.serializers import SubCategorySerializer
from api.serializers import UserSerializer

# Create your views here.
class FanficList(generics.ListCreateAPIView):
    queryset = Fanfic.objects.all()
    serializer_class = FanficSerializer
    name='fanfic-list'


class FanficDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fanfic.objects.all()
    serializer_class = FanficSerializer
    name='fanfic-detail'


class ChapterList(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    name='chapter-list'


class ChapterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fanfic.objects.all()
    serializer_class = ChapterSerializer
    name='chapter-detail'


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name='comment-list'


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name='comment-detail'


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name='category-list'


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name='category-detail'


class SubCategoryList(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    name='subcategory-list'


class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    name='subcategory-detail'


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'fanfics' : reverse('fanfic-list', request=request),
            'chapters': reverse('chapter-list', request=request),
            'comments': reverse(CommentList.name, request=request),
            'category': reverse(CategoryList.name, request=request),
            'sub-category': reverse(SubCategoryList.name, request=request),
            'users': reverse('user-list', request=request),
        })
