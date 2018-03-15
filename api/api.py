import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status, viewsets
from rest_framework.response import Response
from api.serializers import UserSerializer

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
