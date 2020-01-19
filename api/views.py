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

from api.serializers import FlatPagesSerializer, ChangePasswordSerializer, ContentTypeSerializer, NotificationSerializer

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
            'comments': reverse('api:comment-list', request=request),
            'category': reverse('api:category-list', request=request),
            'sub-category': reverse('api:subcategory-list', request=request),
            'tags' : reverse('api:tag-list', request=request),
            'posts' : reverse('api:post-list', request=request),
            'pages': reverse('api:all-pages', request=request),
            'genres': reverse('api:genre-list', request=request),
            'classement': reverse('api:classement-list', request=request),
            'status': reverse('api:status-list', request=request),
            'notifications': reverse('api:notifications', request=request),
            'fanfics': reverse('api:fanfic-list', request=request)
        })
