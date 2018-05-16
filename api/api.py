import json
from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.response import Response
from api.serializers import UserSerializer
from api.serializers import FanficSerializer
from api.serializers import ChangePasswordSerializer
from api.models import Fanfic

# Create your api views here.

class UserCreate(generics.CreateAPIView):
    """
    Create an user
    """
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()


class LoginView(views.APIView):
    """
    Login user
    """
    serializer_class = UserSerializer
    permission_classes = ( permissions.AllowAny,)

    def post(self, request):
        user = authenticate (
            username=request.data.get("username"),
            password=request.data.get("password"))

        if user is None or not user.is_active:
            return Response({
                'status': 'Non autorisé',
                'message': 'Pseudo ou mot de passe incorrect.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response(UserSerializer(user).data)

    # def post(self, request, *args, **kwargs):
    #     login(request, request.user)
    #     return Response(UserSerializer(request.user).data)

class LogoutView(views.APIView):
    """
    Logout user
    """
    permission_classes = ( permissions.AllowAny,)

    def get(self, request):
        logout(request)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class CheckoutUserView(views.APIView):
    """
    Checkout current user
    """
    serializer_class = UserSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        if request.user:
            return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(views.APIView):
  """
  Change password
  """
  permission_classes = (permissions.IsAuthenticated,)

  def get_object(self, queryset=None):
      return self.request.user

  def put(self, request, *args, **kwargs):
      self.object = self.get_object()
      serializer = ChangePasswordSerializer(data=request.data)

      if serializer.is_valid():
          old_password = serializer.data.get('old_password')
          if not self.object.check_password(old_password):
              return Response({'old_password': ['Mot de passe erroné.']}, status=status.HTTP_400_BAD_REQUEST)
          self.object.set_password(serializer.data.get('new_password'))
          self.object.save()
          return Response(status=status.HTTP_204_NO_CONTENT)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def email_feedback(request):
    id = request.data.get('id')
    fanfic = Fanfic.objects.get(id=id)
    msg_html = render_to_string('mail/feedback.html', {'fanfic': fanfic})
    msg_text = ''
    return send_mail('fanfiction signalee', msg_text, 'no-reply@fanfiction.com', ['delita.makanda@gmail.com'], html_message=msg_html, fail_silently=False)


class EmailFeedback(views.APIView):
    """
    Feedback email
    """
    serializer_class = FanficSerializer
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request):
        email_feedback(request)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


def favorited_fanfic(request):
    fanfic_id = request.data.get('id')
    # action = request.data.get('action')
    fanfic = Fanfic.objects.get(id=int(fanfic_id))
    try:
        if fanfic:
            likes = fanfic.likes + 1
        else:
            likes = fanfic.likes - 1
        # elif action == 'love':
            # fanfic.likes *= 2
        fanfic.likes = likes
        fanfic.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
    except:
        pass
    return Response({'status': 'ko'})


class FavoritedFanfic(views.APIView):
    """
    Favorite fanfic
    """
    serializer_class = FanficSerializer()
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        favorited_fanfic(request)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
