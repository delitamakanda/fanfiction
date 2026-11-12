import logging

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts import services
from apps.accounts.api.serializers import (
    AccountProfileSerializer,
    ChangePasswordSerializer,
    ContactMailSerializer,
    DeleteAccountSerializer,
    FollowAuthorInputSerializer,
    FollowStoriesSerializer,
    FollowStoryInputSerializer,
    FollowUserSerializer,
    LoginSerializer,
    LogoutSerializer,
    NotificationSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    RecoConsentSerializer,
    SignupSerializer,
    SocialSerializer,
    UserSerializer,
)
from apps.accounts.models import FollowStories, FollowUser, Notification, Social
from apps.core.permissions import IsOwner
from apps.fanfics import services as fanfic_services
from apps.fanfics.api.serializers import FanficLikeSerializer, FanficListSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


def _error(message, code=status.HTTP_400_BAD_REQUEST):
    if isinstance(message, DjangoValidationError):
        message = " ".join(message.messages)
    return Response({"error": message}, status=code)


# --------------------------------------------------------------------------- #
# Authentication
# --------------------------------------------------------------------------- #


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
        return Response(
            {
                "message": "ok",
                "user": {"id": user.id, "email": user.email, "username": user.username},
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    """Exchange a username (or e-mail) and a password for a JWT pair."""

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return _error("Missing username, email or password")
        user = authenticate(request, **serializer.validated_data)
        if user is None:
            return Response(
                {
                    "status": "Non autorisé",
                    "message": "Pseudo ou mot de passe incorrect.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        User.objects.filter(pk=user.pk).update(last_login=timezone.now())
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {"id": user.id, "email": user.email, "username": user.username},
            }
        )


class LogoutView(generics.GenericAPIView):
    """Blacklist the given refresh token, or every token with ``all``."""

    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["all"]:
            services.blacklist_all_tokens(request.user)
            return Response({"status": "OK, goodbye, all tokens blacklisted"})

        refresh_token = serializer.validated_data.get("refresh_token")
        if not refresh_token:
            return _error("Missing refresh_token")
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError as exc:
            return _error(f"Invalid token {exc}")
        return Response({"status": "OK, goodbye, token blacklisted"})


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        return Response({"message": "Mot de passe mis à jour avec succès."})


class PasswordResetThrottle(AnonRateThrottle):
    scope = "password_reset"


class PasswordResetView(generics.GenericAPIView):
    """Send a reset link by e-mail. Same answer whether the address exists or not."""

    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [PasswordResetThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.send_password_reset_email(serializer.validated_data["email"])
        return Response(
            {
                "message": "If an account uses this address, a reset e-mail has been sent."
            }
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(
        parameters=[
            OpenApiParameter("uidb64", str, OpenApiParameter.PATH),
            OpenApiParameter("token", str, OpenApiParameter.PATH),
        ],
        operation_id="api_v1_accounts_password_reset_confirm",
    )
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return _error("Invalid token or uidb64.")
        if not default_token_generator.check_token(user, token):
            return _error("Invalid token.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["password"])
        user.save(update_fields=["password"])
        logger.info("Password reset for user %s", user.pk)
        return Response({"message": "Password reset successful."})


# --------------------------------------------------------------------------- #
# Current user
# --------------------------------------------------------------------------- #


class CheckoutUserView(generics.RetrieveUpdateAPIView):
    """Read or update the authenticated user and their profile.

    Update payload: ``{"user": {...}, "profile": {...}}``.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        profile = user.accountprofile
        return Response(
            {
                "user": self.get_serializer(user).data,
                "profile": AccountProfileSerializer(profile).data,
                "socials": SocialSerializer(
                    Social.objects.filter(account=profile), many=True
                ).data,
                "followed_authors": FollowUserSerializer(
                    FollowUser.objects.filter(user_from=user).select_related(
                        "user_from", "user_to"
                    ),
                    many=True,
                ).data,
                "followed_fanfics": FollowStoriesSerializer(
                    FollowStories.objects.filter(from_user=user).select_related(
                        "from_user", "to_fanfic"
                    ),
                    many=True,
                ).data,
            }
        )

    def update(self, request, *args, **kwargs):
        user = request.user
        user_serializer = self.get_serializer(
            user, data=request.data.get("user", {}), partial=True
        )
        profile_serializer = AccountProfileSerializer(
            user.accountprofile, data=request.data.get("profile", {}), partial=True
        )
        user_serializer.is_valid(raise_exception=True)
        profile_serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user_serializer.save()
            profile_serializer.save()
        return Response(
            {
                "message": "Utilisateur et profil mis à jour",
                "user": user_serializer.data,
                "profile": profile_serializer.data,
            }
        )


class AcceptRecoConsentView(generics.GenericAPIView):
    serializer_class = RecoConsentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = request.user.accountprofile
        profile.reco_consent_given = serializer.validated_data["reco_consent"]
        profile.save(update_fields=["reco_consent_given"])
        return Response(
            {
                "message": "Consentement accepté",
                "user": UserSerializer(request.user).data,
            }
        )

    patch = put


class DeleteAccountView(generics.GenericAPIView):
    """Deactivate the authenticated account (password confirmation required)."""

    serializer_class = DeleteAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = " ".join(
                str(e) for errors in serializer.errors.values() for e in errors
            )
            return Response({"status": "ko", "message": message}, status=400)
        user = request.user
        blacklisted = services.deactivate_account(
            user, blacklist_tokens=serializer.validated_data["delete_all_tokens"]
        )
        return Response(
            {
                "message": "User deleted successfully",
                "username": user.username,
                "deactivation_date": timezone.now().isoformat(),
                "tokens_blacklisted": blacklisted,
            }
        )


# --------------------------------------------------------------------------- #
# Social networks
# --------------------------------------------------------------------------- #


class SocialCreateApiView(generics.CreateAPIView):
    serializer_class = SocialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(account=user.accountprofile, user=user)


class SocialDestroyApiView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = SocialSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Social.objects.filter(user=self.request.user)


# --------------------------------------------------------------------------- #
# Likes & follows
# --------------------------------------------------------------------------- #


class FanficLikeAPIView(generics.GenericAPIView):
    """``{"id": <fanfic id>, "action": "like" | "unlike"}``."""

    serializer_class = FanficLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=400)
        fanfic = serializer.validated_data["id"]
        liked = serializer.validated_data["action"] == "like"
        fanfic_services.set_like(fanfic, request.user, liked=liked)
        return Response(
            {
                "message": "Fanfic liked." if liked else "Fanfic unliked.",
                "fanfic": FanficListSerializer(fanfic).data,
                "is_liked": liked,
            }
        )


class FollowAuthorAPIView(generics.GenericAPIView):
    """POST follows, DELETE unfollows ``{"user_to_id": <id>}``."""

    serializer_class = FollowAuthorInputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _target(self, request):
        serializer = FollowAuthorInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["user_to"]

    def post(self, request, *args, **kwargs):
        try:
            follow = services.follow_user(request.user, self._target(request))
        except DjangoValidationError as exc:
            return _error(exc)
        return Response(
            FollowUserSerializer(follow).data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        try:
            services.unfollow_user(request.user, self._target(request))
        except DjangoValidationError as exc:
            return _error(exc)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowStoriesAPIView(generics.GenericAPIView):
    """POST follows, DELETE unfollows ``{"to_fanfic_id": <id>}``."""

    serializer_class = FollowStoryInputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _target(self, request):
        serializer = FollowStoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["to_fanfic"]

    def post(self, request, *args, **kwargs):
        try:
            follow = services.follow_story(request.user, self._target(request))
        except DjangoValidationError as exc:
            return _error(exc)
        return Response(
            FollowStoriesSerializer(follow).data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        try:
            services.unfollow_story(request.user, self._target(request))
        except DjangoValidationError as exc:
            return _error(exc)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationListView(generics.ListAPIView):
    """Activity of the users followed by the authenticated user."""

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Notification.objects.none()
        return services.notifications_for(self.request.user)


# --------------------------------------------------------------------------- #
# Contact
# --------------------------------------------------------------------------- #


class ContactFormThrottle(AnonRateThrottle):
    scope = "contact_form"


class ContactMailView(APIView):
    """Send a message to the webmaster (reCAPTCHA protected)."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [ContactFormThrottle]
    serializer_class = ContactMailSerializer

    def post(self, request, *args, **kwargs):
        serializer = ContactMailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        services.send_contact_message(
            name=data["name"],
            email=data["email"],
            subject=data["subject"],
            message=data["message"],
        )
        logger.info("Contact message received")
        return Response({"status": "ok"})
