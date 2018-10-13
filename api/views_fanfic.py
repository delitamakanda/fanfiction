import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from rest_framework.throttling import ScopedRateThrottle
from api.models import Fanfic
from api.serializers import FanficSerializer
from api.serializers import FanficListSerializer
from api import custompermission

from .tasks import fanfic_created

"""
Fanfics
"""

class FanficListByCategory(generics.ListAPIView):
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name='fanfic-list-by-category'

    def get_queryset(self):
        category = self.kwargs['category']
        return Fanfic.objects.filter(category=category, status='publié')


class FanficListBySubCategory(generics.ListAPIView):
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name='fanfic-list-by-subcategory'

    def get_queryset(self):
        subcategory = self.kwargs['subcategory']
        return Fanfic.objects.filter(subcategory=subcategory, status='publié')


class FanficListByAuthor(generics.ListAPIView):
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name='fanfic-list-by-author'

    def get_queryset(self):
        user = self.kwargs['username']
        return Fanfic.objects.filter(author__username=user)


class FanficShowListByAuthorView(generics.ListAPIView):
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name='fanfic-show-list-by-author'

    def get_queryset(self):
        user = self.kwargs['username']
        return Fanfic.objects.filter(author__username=user, status='publié')


class FanficListRemasteredView(generics.ListAPIView):
    """
    Method GET ONLY
    """
    serializer_class = FanficListSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name='fanfic-list-remastered'
    filter_fields = (
        'category',
        'subcategory',
        'status',
    )
    search_fields = (
        '^title',
        '^description',
        '^credits',
        '^synopsis',
    )

    def get_queryset(self):
        return Fanfic.objects.all()


class FanficCreateView(generics.ListCreateAPIView):
    """
    METHOD POST ONLY
    """
    serializer_class = FanficSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        custompermission.IsCurrentAuthorOrReadOnly
    )
    name='fanfic-create'

    def get_queryset(self):
        return Fanfic.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # launch asynchronous tasks
        fanfic_created.delay(serializer.data['id'])
        

"""
method put/delete/get for auth user only
"""

class FanficDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_scope = 'fanfic'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Fanfic.objects.all()
    serializer_class = FanficSerializer
    name='fanfic-detail'
    permission_classes = (
        permissions.IsAuthenticated,
        custompermission.IsCurrentAuthorOrReadOnly,
    )

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

"""
method get for retreive and not update
"""

class FanficListDetailView(generics.RetrieveAPIView):
    throttle_scope = 'fanfic'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Fanfic.objects.all().filter(status='publié')
    serializer_class = FanficListSerializer
    name='fanfic-list-detail'

    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = 'slug'
