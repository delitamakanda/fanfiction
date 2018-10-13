import json
import weasyprint

from django.conf import settings
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.response import Response

from api.models import Fanfic
from api.models import Chapter
from api.models import FollowStories
from api.models import FollowUser

from api.serializers import ChapterSerializer
from api.serializers import FanficSerializer
from api.serializers import FollowStoriesSerializer
from api.serializers import FollowUserSerializer
from api.serializers import ChangePasswordSerializer
from api.serializers import UserSerializer

# Create your api views here.
class EmailFeedbackView(views.APIView):
    """
    Feedback email
    """
    serializer_class = FanficSerializer
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
          send_mail('fanfiction signalee', msg_text, 'no-reply@fanfiction.com', [settings.SERVER_EMAIL], html_message=msg_html, fail_silently=False)
        except BadHeaderError:
          return Response({"status": "invalid header"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
      else:
        return Response({"status": "nok"}, status=status.HTTP_400_BAD_REQUEST)


def liked_fanfic(request):
    fanfic_id = request.data.get('id')
    user = request.data.get('user')

    if fanfic_id and user:
        try:
            fanfic = Fanfic.objects.get(id=int(fanfic_id))

            if fanfic:
                likes = fanfic.users_like.add(user)
            fanfic.users_like = likes
            fanfic.save()
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'status': 'nok'}, status=status.HTTP_400_BAD_REQUEST)


class FavoritedFanficView(views.APIView):
    """
    Favorite fanfic
    """
    serializer_class = FanficSerializer()
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = FanficSerializer()
        if serializer.data:
            liked_fanfic(request)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


def unliked_fanfic(request):
    fanfic_id = request.data.get('id')
    user = request.data.get('user')

    if fanfic_id and user:
        try:
            fanfic = Fanfic.objects.get(id=int(fanfic_id))

            if fanfic:
                likes = fanfic.users_like.remove(user)
            fanfic.users_like = likes
            fanfic.save()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'nok'}, status=status.HTTP_400_BAD_REQUEST)


class UnfavoritedFanficView(views.APIView):
    """
    Unfavorite fanfic
    """
    serializer_class = FanficSerializer()
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = FanficSerializer()
        if serializer.data:
            unliked_fanfic(request)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class FollowUserView(views.APIView):
    """
    Users followed
    """
    authentication_class = ()
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        return list of all authors followed
        """
        try:
            users = FollowUser.objects.all()
            serializer = FollowUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'no content'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer = FollowUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None):
        follow_user_id = request.data.get('id')

        try:
            follow_user = FollowUser.objects.get(id=follow_user_id)
            follow_user.delete()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)


class FollowStoriesView(views.APIView):
  """
  Stories followed
  """
  authentication_class = ()
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request, format=None):
      """
      return list of all stories followed
      """
      try:
          stories = FollowStories.objects.all()
          serializer = FollowStoriesSerializer(stories, many=True)
          return Response(serializer.data, status=status.HTTP_200_OK)
      except:
          return Response({'status': 'no content'}, status=status.HTTP_204_NO_CONTENT)


  def post(self, request):
      serializer = FollowStoriesSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk=None):
      follow_story_id = request.data.get('id')

      try:
          follow_story = FollowStories.objects.get(id=follow_story_id)
          follow_story.delete()
          return Response({'status': 'ok'}, status=status.HTTP_200_OK)
      except:
          return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)




class DeleteAccountView(views.APIView):
    """
    Disable user account
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class ContactMailView(views.APIView):
  """
  Send an email to webmaster
  """
  permission_classes = (permissions.AllowAny,)

  def post(self, request, *args, **kwargs):
    from_email = request.data.get('from_email')
    subject = request.data.get('subject')
    message = request.data.get('message')

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [settings.SERVER_EMAIL])
        except BadHeaderError:
            return Response({"status": "invalid headers"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "nok"}, status=status.HTTP_400_BAD_REQUEST)


class PrintFanficToPDFView(views.APIView):
    """
    Generate a pdf output of fanfic current fanfic
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk=None):
        try:
            fanfic = Fanfic.objects.get(id=pk)
            chapters = Chapter.objects.filter(fanfic=fanfic)
            html = render_to_string('pdf/fanfic.html', {'fanfic': fanfic, 'chapters': chapters})
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="fanfic_{}.pdf"'.format(fanfic.id)
            weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/styles/base.css')])
            return response
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)
