from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.accounts import services
from apps.accounts.models import (
    AccountProfile,
    FollowStories,
    FollowUser,
    Notification,
    Social,
)
from apps.chapters.models import Chapter
from apps.fanfics.api.serializers import FanficListSerializer
from apps.fanfics.models import Fanfic

User = get_user_model()

MAX_PHOTO_SIZE = 5 * 1024 * 1024


# --------------------------------------------------------------------------- #
# Users & profiles
# --------------------------------------------------------------------------- #


class PublicUserSerializer(serializers.ModelSerializer):
    """What anyone may know about another user."""

    class Meta:
        model = User
        fields = ("id", "username")
        read_only_fields = fields


class UserFanficSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = fields


class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = (
            "id",
            "bio",
            "photo",
            "date_of_birth",
            "location",
            "reco_consent_given",
        )
        read_only_fields = ("id",)

    def validate_photo(self, value):
        if value and value.size > MAX_PHOTO_SIZE:
            raise serializers.ValidationError(
                "Image file too large. Maximum size is 5MB."
            )
        return value


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ("id", "network", "nichandle", "account", "user")
        read_only_fields = ("id", "account", "user")

    def validate_network(self, value):
        request = self.context.get("request")
        if request is None or self.instance is not None:
            return value
        if Social.objects.filter(network=value, user=request.user).exists():
            raise serializers.ValidationError("Ce réseau social est déjà renseigné.")
        return value


class UserSerializer(serializers.ModelSerializer):
    """The authenticated user (``/accounts/user/``)."""

    profile = AccountProfileSerializer(source="accountprofile", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "profile",
        )
        read_only_fields = ("id", "username", "email", "date_joined", "profile")


class FollowUserSerializer(serializers.ModelSerializer):
    user_from = UserFanficSerializer(read_only=True)
    user_to = UserFanficSerializer(read_only=True)

    class Meta:
        model = FollowUser
        fields = ("id", "user_from", "user_to", "created")
        read_only_fields = fields


class FollowStoriesSerializer(serializers.ModelSerializer):
    from_user = UserFanficSerializer(read_only=True)
    to_fanfic = FanficListSerializer(read_only=True)

    class Meta:
        model = FollowStories
        fields = ("id", "from_user", "to_fanfic", "created")
        read_only_fields = fields


@extend_schema_field(OpenApiTypes.STR)
class NotificationTargetField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, User):
            return value.username
        if isinstance(value, Chapter | Fanfic):
            return value.title
        return str(value)


class NotificationSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    target = NotificationTargetField(read_only=True)

    class Meta:
        model = Notification
        fields = (
            "id",
            "user",
            "verb",
            "target",
            "target_ct",
            "target_id",
            "read",
            "created",
        )
        read_only_fields = fields


# --------------------------------------------------------------------------- #
# Inputs of the action endpoints
# --------------------------------------------------------------------------- #


class FollowAuthorInputSerializer(serializers.Serializer):
    user_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True), source="user_to"
    )


class FollowStoryInputSerializer(serializers.Serializer):
    to_fanfic_id = serializers.PrimaryKeyRelatedField(
        queryset=Fanfic.published.all(), source="to_fanfic"
    )


class RecoConsentSerializer(serializers.Serializer):
    reco_consent = serializers.BooleanField(default=True)


# --------------------------------------------------------------------------- #
# Authentication
# --------------------------------------------------------------------------- #


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {"email": {"required": True, "allow_blank": False}}

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords did not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username or e-mail address")
    password = serializers.CharField(style={"input_type": "password"})


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=False, allow_blank=True)
    all = serializers.BooleanField(default=False)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mot de passe erroné.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    delete_all_tokens = serializers.BooleanField(default=True)

    def validate_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Password is incorrect")
        return value


# --------------------------------------------------------------------------- #
# Contact form
# --------------------------------------------------------------------------- #

_LENGTH_ERRORS = {
    "name": "Le nom doit contenir entre 2 et 100 caractères",
    "message": "Le message doit contenir entre 10 et 5000 caractères",
    "subject": "Le sujet doit contenir entre 1 et 200 caractères",
}


class ContactMailSerializer(serializers.Serializer):
    name = serializers.CharField(
        min_length=2,
        max_length=100,
        error_messages={
            "min_length": _LENGTH_ERRORS["name"],
            "max_length": _LENGTH_ERRORS["name"],
            "required": "Le nom est requis",
            "blank": "Le nom est requis",
        },
    )
    email = serializers.EmailField(
        max_length=254,
        error_messages={
            "invalid": "Veuillez entrer une adresse email valide",
            "required": "L'adresse email est requise",
            "blank": "L'adresse email est requise",
        },
    )
    message = serializers.CharField(
        min_length=10,
        max_length=5000,
        error_messages={
            "min_length": _LENGTH_ERRORS["message"],
            "max_length": _LENGTH_ERRORS["message"],
            "required": "Le message est requis",
            "blank": "Le message est requis",
        },
    )
    subject = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        error_messages={"max_length": _LENGTH_ERRORS["subject"]},
    )
    captcha_token = serializers.CharField(
        write_only=True, error_messages={"required": "Le token de captcha est requis"}
    )

    def validate_name(self, value):
        if not value.replace(" ", "").replace("-", "").isalpha():
            raise serializers.ValidationError(
                "Le nom ne peut contenir que des lettres et des espaces"
            )
        return value

    def validate_message(self, value):
        lowered = value.lower()
        if "http://" in lowered or "https://" in lowered:
            raise serializers.ValidationError(
                "Le message ne peut pas contenir de liens"
            )
        return value

    def validate_captcha_token(self, value):
        if not services.verify_recaptcha(value):
            raise serializers.ValidationError("Veuillez valider le captcha")
        return value

    def validate(self, attrs):
        if not attrs.get("subject"):
            attrs["subject"] = f"Message de contact - {attrs['name']}"
        return attrs
