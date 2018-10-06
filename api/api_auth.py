import json

from django.shortcuts import render, HttpResponse
from django.core.mail import mail_admins
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.response import Response
from api.serializers import ChangePasswordSerializer
from api.serializers import UserSerializer

from api.models import AccountProfile

# Create your api views here.
class UserCreateView(generics.CreateAPIView):
    """
    Create an user
    """
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        mail_admins("Account creation", "An user has created an account.")
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class LoginView(views.APIView):
    """
    Login user
    """
    serializer_class = UserSerializer
    permission_classes = ( permissions.AllowAny,)

    def post(self, request):
        profile = AccountProfile.objects.all()

        user = authenticate (
            username=request.data.get("username"),
            password=request.data.get("password"))

        if user is None or not user.is_active:
            return Response({
                'status': 'Non autorisé',
                'message': 'Pseudo ou mot de passe incorrect.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not profile.filter(user=user).exists():
            AccountProfile.objects.create(user=user)

        login(request, user)
        return Response(UserSerializer(user).data)


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
  Change password view
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
