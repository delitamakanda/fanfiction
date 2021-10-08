from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.contenttypes.models import ContentType

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.serializers import FlatPagesSerializer, ContentTypeSerializer, NotificationSerializer
from fanfics.api.serializers import FanficSerializer
from categories.api.serializers import CategorySerializer

from api.models import FlatPages, Notification
from fanfics.models import Fanfic
from categories.models import Category

from api.recommender import Recommender

class EmailFeedbackView(views.APIView):
    """
    Feedback email
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args,  **kwargs):
        id = request.data.get('id')
        fanfic = Fanfic.objects.get(id=id)

        template = get_template('mail/feedback.txt')
        context = {'fanfic': fanfic}

        msg_text = template.render(context)
        msg_html = render_to_string('mail/feedback.html', context)

        if fanfic:
            try:
                send_mail('fanfiction signalee', msg_text, 'no-reply@fanfiction.com',
                          [settings.SERVER_EMAIL], html_message=msg_html, fail_silently=False)
            except BadHeaderError:
                return Response({"status": "invalid header"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "nok"}, status=status.HTTP_400_BAD_REQUEST)


class ContactMailView(views.APIView):
    """
    Send an email to webmaster
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        from_email = request.data.get('from_email')
        subject = request.data.get('subject')
        message = request.data.get('message')

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email,
                          [settings.SERVER_EMAIL])
            except BadHeaderError:
                return Response({"status": "invalid headers"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "nok"}, status=status.HTTP_400_BAD_REQUEST)


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
        following_ids = self.request.user.following.values_list(
            'id', flat=True)

        if following_ids:
            notifications = notifications.filter(user_id__in=following_ids).select_related(
                'user', 'user__accountprofile').prefetch_related('target')

        notifications = notifications[:20]

        return notifications


class BrowseFanfictionListView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        liked_fanfics = Fanfic.objects.filter(
            status='publié').order_by('-total_likes')[:10]
        newest_fanfics = Fanfic.objects.filter(
            status='publié').order_by('-publish')[:10]

        r = Recommender()
        recommended_fanfics = r.suggest_fanfics_for([fanfic for fanfic in Fanfic.objects.filter(status='publié')], 10)
        categories = Category.objects.all()

        LikedSerializerData = FanficSerializer(liked_fanfics, many=True)
        newSerializerData = FanficSerializer(newest_fanfics, many=True)
        recoSerializerData = FanficSerializer(recommended_fanfics, many=True)
        categorySerializerData = CategorySerializer(categories, many=True)

        return Response({'recommended_fanfics': recoSerializerData.data, 'most_liked_fanfics': LikedSerializerData.data, 'newest_fanfics': newSerializerData.data, 'all_categories': categorySerializerData.data})
