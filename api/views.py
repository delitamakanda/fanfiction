import json

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.contenttypes.models import ContentType
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter

from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse

from fanfics.models import Fanfic
from api.models import FlatPages, Notification

from api.serializers import FlatPagesSerializer
from api.serializers import NotificationSerializer
from api.serializers import ContentTypeSerializer

from api import custompermission

"""
FlatPages
"""

class FlatPagesView(generics.ListAPIView):
    """docstring for FlatPagesView."""
    queryset = FlatPages.objects.all()
    serializer_class = FlatPagesSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name = 'all-pages'


class FlatPagesByTypeView(generics.RetrieveAPIView):
    """docstring for FlatPagesByTypeView."""
    queryset = FlatPages.objects.all()
    serializer_class = FlatPagesSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = 'type'
    name = 'pages'


@method_decorator(xframe_options_exempt, name='dispatch')
class FlatPagesHTMLByTypeView(generics.RetrieveAPIView):
    """docstring for FlatPagesHTMLByTypeView."""
    queryset = FlatPages.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = 'type'
    name = 'pages'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'page': self.object}, template_name='webview/static_pages.html')



"""
Notification generics views
"""

class ContentTypeView(generics.RetrieveAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    def get_queryset(self):
        notifications = Notification.objects.exclude(user=self.request.user)
        # print(notifications)
        following_ids = self.request.user.following.values_list('id', flat=True)

        if following_ids:
            notifications = notifications.filter(user_id__in=following_ids).select_related('user', 'user__accountprofile').prefetch_related('target')

        notifications = notifications[:20]

        return notifications




class ApiRootView(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'fanfics-list-remastered': reverse('fanfic-list-remastered', request=request),
            'chapters': reverse('chapter-create', request=request),
            'comments': reverse('comment-list', request=request),
            'category': reverse('category-list', request=request),
            'sub-category': reverse('subcategory-list', request=request),
            'users': reverse('user-list', request=request),
            'tags' : reverse('tag-list', request=request),
            'posts' : reverse('post-list', request=request),
            'pages': reverse('all-pages', request=request),
            'genres': reverse('genre-list', request=request),
            'comments-by-chapter-create': reverse('comment-by-chapter-create', request=request),
            'notifications': reverse('notifications', request=request)

        })
