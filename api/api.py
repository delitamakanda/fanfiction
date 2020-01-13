import json

from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import get_template

from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.response import Response

from fanfics.models import Fanfic
from chapters.models import Chapter

from accounts.models import FollowStories, FollowUser

from fanfics.api.serializers import FanficSerializer
from accounts.api.serializers import FollowStoriesSerializer, FollowUserSerializer
from api.serializers import ChangePasswordSerializer
from accounts.api.serializers import UserSerializer


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
	# serializer_class = FanficSerializer()
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        """
        return list of all authors followed
        """
        try:
            follow_users = FollowUser.objects.all()
            serializer = FollowUserSerializer(follow_users, many=True)
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
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
