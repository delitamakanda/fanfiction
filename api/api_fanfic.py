from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, send_mail

from rest_framework import permissions, views, status
from rest_framework.response import Response

from fanfics.models import Fanfic

class ShareFanficAPIView(views.APIView):
    """
    Share fanfiction with e-mail
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        fanfic_id = request.data.get('id')
        fanfic = Fanfic.objects.get(id=fanfic_id)
        current_site = get_current_site(request)

        name = request.data.get('name')
        email = request.data.get('email')
        to = request.data.get('to')
        comments = request.data.get('comments')

        try:
            fanfic_url = current_site.domain + '/#/' + 'fanfic/detail/' + fanfic.slug
            subject = '{} ({}) recommends you reading "{}"'.format(name, email, fanfic.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(fanfic.title, fanfic_url,name, comments)
            send_mail(subject, message, settings.SERVER_EMAIL, [to])
            sent = True
            return Response({"message": sent}, status=status.HTTP_200_OK)
        except BadHeaderError:
            return Response({"status": "invalid headers"}, status=status.HTTP_400_BAD_REQUEST)
