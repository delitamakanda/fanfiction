from django.http import BadHeaderError
from django.template.loader import render_to_string, get_template
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from rest_framework import generics, filters, status, views
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import send_mail

from fanfics.models import Fanfic, Recommendation

from fanfics.api.serializers import  FanficListSerializer, FanficCreateSerializer, FanficDetailSerializer
from fanfics.api.filters import FanficFilter

from api import custompermission, custompagination

import logging

logger = logging.getLogger(__name__)


class ChoicesViewSet(ViewSet):
    permission_classes = [AllowAny,]
    choices = []
    response_key = None

    def list(self, request):
        data = [{ id: id, 'libelle': libelle } for id, libelle in self.choices]
        return Response({self.response_key: data})


class GenresViewSet(ChoicesViewSet):
    choices = Fanfic.GENRES_CHOICES
    response_key = 'genres'


class ClassementViewSet(ChoicesViewSet):
    choices = Fanfic.CLASSEMENT_CHOICES
    response_key = 'classement'


class StatusViewSet(ChoicesViewSet):
    choices = Fanfic.STATUS_CHOICES
    response_key ='status'


class FanficViewSet(ModelViewSet):
    queryset = Fanfic.objects.all()
    filter_class = FanficFilter
    pagination_class = custompagination.StandardResultsSetPagination
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    throttle_scope = 'anon'
    throttle_classes = (ScopedRateThrottle,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        'title',
        'status',
        '^description',
        '^synopsis',
        'author__username',
    ]
    ordering_fields = [
        'created',
        'total_likes',
        'views',
        'updated',
    ]
    permission_classes = (
        custompermission.IsCurrentAuthorOrReadOnly,
    )

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return FanficCreateSerializer
        elif self.action == 'retrieve':
            return FanficDetailSerializer
        return FanficListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        session_key = 'viewed_fanfic_{}'.format(instance.pk)
        if not self.request.session.get(session_key, False):
            instance.views += 1
            instance.save()
            self.request.session[session_key] = True
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class ShareFanficAPIView(views.APIView):
    """
    Share fanfiction with e-mail
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            fanfic_id = request.data.get('id')
            fanfic = Fanfic.objects.get(id=fanfic_id)
            current_site = get_current_site(request)

            name = request.data.get('name')
            email = request.data.get('email')
            to_email = request.data.get('to_email')
            comments = request.data.get('comments')

            fanfic_url = current_site.domain + '/#/' + 'fanfic/' + fanfic.slug
            subject = '{} ({}) recommends you reading "{}"'.format(name, email, fanfic.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(fanfic.title, fanfic_url, name, comments)
            send_mail(subject, message, settings.SERVER_EMAIL, [to_email])
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BadHeaderError as e:
            logger.warning(f"Invalid header: {str(e)}")
            return Response({"status": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Fanfic.DoesNotExist:
            logger.warning(f"Fanfic does not exist")
            return Response({"status": "Fanfic does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailFeedbackView(views.APIView):
    """
    Feedback email
    """
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @staticmethod
    def post(self, request, *args, **kwargs):
        try:
            fanfic_id = request.data.get('id')
            fanfic = Fanfic.objects.get(id=fanfic_id)

            template = get_template('mail/feedback.txt')
            context = {'fanfic': fanfic}

            msg_text = template.render(context)
            msg_html = render_to_string('mail/feedback.html', context)

            send_mail('fanfiction signalee', msg_text, 'no-reply@fanfiction.com',[settings.SERVER_EMAIL], html_message=msg_html, fail_silently=False)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        except BadHeaderError:
            logger.warning(f"Invalid header")
            return Response({"status": "invalid header"}, status=status.HTTP_400_BAD_REQUEST)
        except Fanfic.DoesNotExist:
            logger.warning(f"Fanfic does not exist")
            return Response({"status": "Fanfic does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRecommendationsAPIView(generics.ListAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = FanficListSerializer

    def get_queryset(self):
        if not self.request.user.accountprofile.reco_consent_given:
            return Response({"message": "You must give consent to receive recommendations"}, status=status.HTTP_403_FORBIDDEN)
        try:
            recs = Recommendation.objects.filter(user=self.request.user)
            serializer = self.get_serializer(recs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        Recommendation.objects.filter(user=self.request.user).delete()
        cache.delete(f"recs_{self.request.user.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

