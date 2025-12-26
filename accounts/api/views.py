from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.http import BadHeaderError
from django.http.response import Http404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.api.serializers import AccountProfileSerializer, FollowStoriesSerializer, FollowUserSerializer, \
    SignupSerializer, SocialSerializer, UserSerializer, ChangePasswordSerializer, NotificationSerializer, \
    PasswordResetSerializer, ContactMailSerializer, DeleteAccountSerializer
from accounts.models import FollowUser, FollowStories, Social, Notification
from api import custompermission, custompagination
from fanfics.api.serializers import FanficSerializer
from fanfics.models import Fanfic
import logging

logger = logging.getLogger(__name__)


class PasswordResetView(generics.GenericAPIView):
    """
    Allows users to reset their passwords.
    """
    permission_classes = (permissions.AllowAny,)
    @staticmethod
    def post(request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            user = result['user']
            token = result['token']
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            protocol = request.is_secure() and 'https' or 'http'
            link = f'{protocol}://{request.get_host()}/api/accounts/password_reset/{uidb64}/{token}/'
            send_mail(
                'Password reset request',
                f'To reset your password, visit this link: {link}',
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            return Response({'message': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialDestroyApiView(generics.UpdateAPIView,generics.DestroyAPIView):
    """
    Destroy a social account
    """
    serializer_class = SocialSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        custompermission.IsCurrentUserOrReadonly,
    )
    authentication_classes = ()

    def get_queryset(self):
        try:
            return Social.objects.filter(account=self.request.user.accountprofile)
        except Social.DoesNotExist:
            raise Http404("Social account not found.")

    def get_object(self):
        try:
            return self.get_queryset().get(id=self.kwargs.get('pk'))
        except Social.DoesNotExist:
            raise Http404("Social account not found.")


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (custompermission.IsAuthenticatedOrCreate,)
    authentication_classes = ()

    @transaction.atomic
    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response({
                "message": "ok",
                "user": {
                    "id": serializer.instance.id,
                    "email": serializer.instance.email,
                    "username": serializer.instance.username,

                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def liked_fanfic(request):
    fanfic_id = request.data.get('id')
    user_id = request.data.get('user')

    if fanfic_id and user_id:
        try:
            fanfic = Fanfic.objects.get(id=int(fanfic_id))

            if fanfic:
                likes = fanfic.users_like.add(user_id)
                fanfic.users_like = likes
                fanfic.save()
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'status': 'nok'}, status=status.HTTP_400_BAD_REQUEST)


class FavoritedFanficView(generics.GenericAPIView):
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
        return Response(serializer.data, status=status.HTTP_200_OK)


def unliked_fanfic(request):
    fanfic_id = request.data.get('id')
    user_id = request.data.get('user')

    if fanfic_id and user_id:
        try:
            fanfic = Fanfic.objects.get(id=int(fanfic_id))

            if fanfic:
                likes = fanfic.users_like.remove(user_id)
                fanfic.users_like = likes
                fanfic.save()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'nok'}, status=status.HTTP_400_BAD_REQUEST)


class UnfavoritedFanficView(generics.GenericAPIView):
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
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostFollowAuthor(generics.CreateAPIView):
    """
    Follow an author
    """
    serializer_class = FollowUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UnFollowAuthor(generics.DestroyAPIView):
    """
    Unfollow an author
    """
    serializer_class = FollowUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'user_from__username'


class FollowUserView(generics.GenericAPIView):
    """
    Users followed
    """
    serializer_class = FollowUserSerializer
    pagination_class = custompagination.StandardResultsSetPagination
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, username, format=None):
        """
        return list of all authors followed
        """
        try:
            follow_users = FollowUser.objects.filter(user_from__username=username)
            serializer = FollowUserSerializer(follow_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'no content'}, status=status.HTTP_204_NO_CONTENT)


    def delete(self, request, pk=None):
        follow_user_id = request.data.get('id')

        try:
            follow_user = FollowUser.objects.get(id=follow_user_id)
            follow_user.delete()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'ko'}, status=status.HTTP_400_BAD_REQUEST)

class FollowAuthorDeleteView(generics.GenericAPIView):
    """
    Author followed
    """
    serializer_class = FollowUserSerializer()
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get_object(self, request, user_to):
        user_from = request.data.get('user_from')
        try:
            return FollowUser.objects.get(user_to=user_to, user_from=user_from)
        except FollowUser.DoesNotExist:
            raise Http404

    def get(self, request, user_to, format=None):
        author_followed = self.get_object(request, user_to)
        serializer = FollowUserSerializer(author_followed)
        return Response(serializer.data)

    def delete(self, request, user_to, format=None):
        author_followed = self.get_object(request, user_to)
        author_followed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowStoriesDeleteView(generics.GenericAPIView):
    """
    Author followed
    """
    serializer_class = FollowStoriesSerializer()
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get_object(self, request, to_fanfic):
        from_user = request.data.get('from_user')
        try:
            return FollowStories.objects.get(to_fanfic=to_fanfic, from_user=from_user)
        except FollowStories.DoesNotExist:
            raise Http404

    def get(self, request, to_fanfic, format=None):
        story_followed = self.get_object(request, to_fanfic)
        serializer = FollowStoriesSerializer(story_followed)
        return Response(serializer.data)

    def delete(self, request, to_fanfic, format=None):
        story_followed = self.get_object(request, to_fanfic)
        story_followed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowStoriesView(generics.GenericAPIView):
    """
    Stories followed
    """
    serializer_class = FollowStoriesSerializer
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def get(self, request, username, format=None):
        """
        return list of all stories followed
        """
        try:
            stories = FollowStories.objects.filter(from_user__username=username)
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


class DeleteAccountView(generics.GenericAPIView):
    """
    Disable user account
    """
    serializer_class = DeleteAccountSerializer
    permission_classes = (permissions.IsAuthenticated, custompermission.IsUserOrReadonly,)
    authentication_classes = ()

    def get_object(self):
        return self.request.user

    def _validate_password(self, user, password):
        if not password:
            raise serializers.ValidationError("Password is required")

        if not user.check_password(password):
            raise serializers.ValidationError("Password is incorrect")

    def _blacklist(self, user):
        try:
            outstanding_token = OutstandingToken.objects.filter(user=user)
            for token in outstanding_token:
                BlacklistedToken.objects.get_or_create(token=token)
            return outstanding_token.count()
        except Exception as e:
            logger.error("Error while blacklisting tokens: %s", str(e))
            return 0

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        password = request.data.get('password')
        delete_all_tokens = request.data.get('delete_all_tokens', False)
        try:
            self._validate_password(user, password)
            tokens_blacklisted = 0
            if delete_all_tokens:
                tokens_blacklisted = self._blacklist(user)
            user.is_active = False
            user.save()
            email_sent = self._send_confirmation_email(user)
            logger.info(
                f"User {user.username} has been deleted. {tokens_blacklisted} tokens have been blacklisted. Token deletion: {delete_all_tokens}. email: {'ok' if email_sent else 'failed'}."
            )
            return Response({
                "message": "User deleted successfully",
                "username": user.username,
                "deactivation_date": timezone.now().isoformat(),
                "tokens_blacklisted": tokens_blacklisted
            }, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            logger.warning("Error while validating password: %s", str(e)  )
            return Response({'status': 'ko','message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error while deleting user: %s", str(e))
            return Response({'status': 'ko'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def _send_confirmation_email(self, user):
        try:
            subject = 'Account deactivation'
            context = {
                'username': user.username,
                'email': user.email,
                'deactivation_date': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

            html_template = render_to_string('mail/account_deletion.html', context)

            send_mail(
                subject,
                f'Account deactivation - {user.username}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_template,
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error("Error while sending confirmation email: %s", str(e))
            return False



class LoginView(generics.GenericAPIView):
    """
    Login user
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    @staticmethod
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({
                "error": "Missing username, email or password",
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"))

        if user is None or not user.is_active:
            return Response({
                'status': 'Non autorisé',
                'message': 'Pseudo ou mot de passe incorrect.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = RefreshToken.for_user(user)
        return Response({
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        }, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    """
    Logout user
    """
    permission_classes = (custompermission.IsAuthenticatedOrCreate, permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            if request.data.get("all"):
                for token in OutstandingToken.objects.filter(user=request.user):
                    BlacklistedToken.objects.get_or_create(token=token)
                return Response({"status": "OK, goodbye, all tokens blacklisted"}, status=status.HTTP_200_OK)

            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Missing refresh_token"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status": "OK, goodbye, token blacklisted"}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error": f"Invalid token {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckoutUserView(generics.RetrieveUpdateAPIView):
    """
    Checkout current user
    """
    serializer_class = UserSerializer
    permission_classes = (custompermission.IsAuthenticatedOrCreate, custompermission.IsUserOrReadonly,)
    authentication_classes = ()

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['profile'] = self.request.user.accountprofile
        return context

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user_data = request.data.get('user', {})
        profile_data = request.data.get('profile', {})
        serializer = self.get_serializer(user, data=user_data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer2 = AccountProfileSerializer(user.accountprofile, data=profile_data, partial=True)
        if not serializer2.is_valid():
            return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer2.save()
        return Response({
            'message': 'Utilisateur et profil mis à jour',
            'user': serializer.data,
                'profile': serializer2.data,
            }, status=status.HTTP_200_OK,)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(
            {
                'user': serializer.data,
                'profile': AccountProfileSerializer(user.accountprofile).data,
                'social_nichandles': SocialSerializer(Social.objects.filter(account=user.accountprofile), many=True).data,
            }, status=status.HTTP_200_OK,
        )




class ChangePasswordView(generics.GenericAPIView):
    """
    Change password view
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

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



class ContactFormThrottle(AnonRateThrottle):
    scope = 'contact_form'
    rate = '5/hour'
    description = '5 emails per hour'

class ContactMailView(generics.GenericAPIView):
    """
    Send an email to webmaster
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = ContactMailSerializer
    throttle_classes = [ContactFormThrottle,]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            name = serializer.validated_data['name']

            formatted_message = f"De: {name} <{email}>\n\nSujet: {subject}\n\nMessage:\n{message}"

            send_mail(subject, formatted_message, from_email=email,
                      recipient_list=[settings.SERVER_EMAIL], fail_silently=False)
            logger.info(f"Email sent from {email} with subject {subject}")
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        except BadHeaderError as e:
            logger.warning(f"Invalid header in email: {str(e)}")
            return Response({"status": "invalid headers"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"An error occurred while sending email: {str(e)}")
            return Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""
Notification generics views
"""

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        notifications = Notification.objects.exclude(user=self.request.user)
        following_ids = self.request.user.following.values_list(
            'id', flat=True)

        if following_ids:
            notifications = notifications.filter(user_id__in=following_ids).select_related(
                'user', 'user__accountprofile').prefetch_related('target')

        notifications = notifications[:20]

        return notifications
