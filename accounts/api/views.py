from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.http import BadHeaderError
from django.http.response import Http404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uuid64 = urlsafe_base64_encode(force_bytes(user.pk))

                protocol = request.is_secure() and 'https' or 'http'
                domain = request.get_host()
                reset_url = f'{protocol}://{domain}/#/password_reset/{uuid64}/{token}/'
                context = {
                    'user': user.username,
                    'reset_url': reset_url,
                    'domain': domain,
                    'uid': uuid64,
                    'token': token,
                    'protocol': protocol,
                }

                html_message = render_to_string('registration/password_reset_email.html', context)

                send_mail(
                    'Password reset request',
                    f'To reset your password, visit this link: {reset_url}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                logger.info(f'Password reset email sent to {user.email}')
                return Response({'message': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist as e:
                logger.warning(f'User does not exist: {str(e)}')
                return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            return Response({'error': 'Invalid token or uidb64.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({
                'error': 'Invalid token.'
            }, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password or new_password!= confirm_password:
            return Response({
                'error': 'Passwords do not match.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user.set_password(new_password)
            user.save()
            logger.info(f'Password reset for user {user.username}')
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error resetting password for user {user.username}: {str(e)}')
            return Response({'error': 'An error occurred while resetting password.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SocialCreateApiView(generics.CreateAPIView):
    """
    Create a social account
    """
    serializer_class = SocialSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        try:
            serializer.save(account=self.request.user.accountprofile, user=self.request.user)
        except AttributeError as e:
            raise serializers.ValidationError(str(e))


class SocialDestroyApiView(generics.UpdateAPIView, generics.DestroyAPIView):
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


class FanficLikeAPIView(generics.GenericAPIView):
    serializer_class = FanficSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Fanfic.objects.all()

    def get_object(self):
        fanfic_id = self.request.data.get('id')
        if not fanfic_id:
            raise serializers.ValidationError('Fanfic ID is required.')
        try:
            return Fanfic.objects.get(id=fanfic_id)
        except (Fanfic.DoesNotExist, ValueError):
            raise serializers.ValidationError('Fanfic not found.')

    def post(self, request, *args, **kwargs):
        action = request.data.get('action') # like or unlike

        if action not in ['like', 'unlike']:
            return Response({'error': 'Invalid action. Use either "like" or "unlike".'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fanfic = self.get_object()
            if action == 'like':
                fanfic.users_like.add(request.user)
                message = 'Fanfic liked.'
            else:
                fanfic.users_like.remove(request.user)
                message = 'Fanfic unliked.'

            serializer = self.get_serializer(fanfic)
            return Response({
                    'message': message,
                    'fanfic': serializer.data,
                'is_liked': fanfic.users_like.filter(id=request.user.id).exists(),
            }, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error('An error occurred: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowAuthorAPIView(generics.GenericAPIView):
    """
    Unfollow an author
    """
    serializer_class = FollowUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = FollowUser.objects.all()

    def get_object(self):
        user_to_id = self.request.data.get('user_to_id')
        if not user_to_id:
            raise serializers.ValidationError('User to follow ID is required.')
        try:
            return FollowUser.objects.get(
                user_from=self.request.user,
                user_to=user_to_id,
            )
        except FollowUser.DoesNotExist:
            return None


    def post(self, request, *args, **kwargs):
        user_to_id = self.request.data.get('user_to_id')
        if not user_to_id:
            return Response({'error': 'User to follow ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            follow_user = self.get_object()
            if follow_user:
                return Response({'error': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)
            follow_user = FollowUser.objects.create(
                user_from=self.request.user,
                user_to=user_to_id,
            )
            serializer = self.get_serializer(follow_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error('An error occurred: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        follow_user = self.get_object()
        if not follow_user:
            return Response({'error': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follow_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error('An error occurred: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FollowStoriesAPIView(generics.GenericAPIView):
    """
    Author followed
    """
    serializer_class = FollowStoriesSerializer()
    permission_classes = (permissions.IsAuthenticated,)
    queryset = FollowStories.objects.all()

    def get_object(self):
        to_fanfic_id = self.request.data.get('to_fanfic_id')
        if not to_fanfic_id:
            raise serializers.ValidationError('Fanfic ID is required.')
        try:
            return FollowStories.objects.get(to_fanfic=to_fanfic_id, from_user=self.request.user)
        except FollowStories.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        to_fanfic_id = request.data.get('to_fanfic_id')
        if not to_fanfic_id:
            return Response({'error': 'Fanfic ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            follow_stories = self.get_object()
            if follow_stories:
                return Response({'error': 'You are already following this fanfic.'}, status=status.HTTP_400_BAD_REQUEST)
            follow_stories = FollowStories.objects.create(to_fanfic=to_fanfic_id, from_user=self.request.user)
            serializer = self.get_serializer(follow_stories)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error('An error occurred: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        follow_stories = self.get_object()
        if not follow_stories:
            return Response({'error': 'You are not following this fanfic.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            follow_stories.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error('An error occurred: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            logger.warning("Error while validating password: %s", str(e))
            return Response({'status': 'ko', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
        }, status=status.HTTP_200_OK, )

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(
            {
                'user': serializer.data,
                'profile': AccountProfileSerializer(user.accountprofile).data,
                'socials': SocialSerializer(Social.objects.filter(account=user.accountprofile), many=True).data,
                'followed_authors': FollowUserSerializer(FollowUser.objects.filter(user_from=user), many=True).data,
                'followed_fanfics': FollowStoriesSerializer(FollowStories.objects.filter(from_user=user), many=True).data,
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
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        old_password = serializer.data.get('old_password')
        if not user.check_password(old_password):
            return Response({'old_password': ['Mot de passe erroné.']}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get('new_password'))
        user.save(update_fields=['password'])
        return Response({
            'message': 'Mot de passe mis à jour avec succès.'
        },status=status.HTTP_200_OK)


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
    throttle_classes = [ContactFormThrottle, ]

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
    serializer_class = NotificationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    pagination_class = custompagination.StandardResultsSetPagination

    def get_queryset(self):
        following_ids = self.request.user.following.values_list(
            'id', flat=True)

        return Notification.objects.filter(
            user_id__in=following_ids
        ).select_related(
            'user',
            'user__accountprofile',
        ).prefetch_related(
            'target',
        ).order_by('-created')
