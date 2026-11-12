import logging

from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from apps.core.permissions import IsOwnerOrReadOnly
from apps.fanfics import services
from apps.fanfics.api.filters import FanficFilter
from apps.fanfics.api.serializers import (
    ChoiceSerializer,
    FanficDetailSerializer,
    FanficListSerializer,
    FanficReferenceSerializer,
    FanficWriteSerializer,
    ShareFanficSerializer,
)
from apps.fanfics.models import Fanfic

logger = logging.getLogger(__name__)


class ChoicesViewSet(viewsets.ViewSet):
    """Read-only list of choices: ``{<response_key>: [{"id", "libelle"}]}``."""

    permission_classes = [permissions.AllowAny]
    choices: tuple = ()
    response_key = ""

    @extend_schema(responses=ChoiceSerializer(many=True))
    def list(self, request):
        data = [{"id": value, "libelle": label} for value, label in self.choices]
        return Response({self.response_key: data})


class GenresViewSet(ChoicesViewSet):
    choices = Fanfic.GENRES_CHOICES
    response_key = "genres"


class ClassementViewSet(ChoicesViewSet):
    choices = Fanfic.CLASSEMENT_CHOICES
    response_key = "classement"


class StatusViewSet(ChoicesViewSet):
    choices = Fanfic.STATUS_CHOICES
    response_key = "status"


class FanficViewSet(viewsets.ModelViewSet):
    """Fanfics, looked up by slug.

    Readers only see published fanfics; authors also see their drafts.
    Only the author can update or delete a fanfic.
    """

    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_class = FanficFilter
    search_fields = ["title", "status", "^description", "^synopsis", "author__username"]
    ordering_fields = ["created", "total_likes", "views", "updated"]

    def get_queryset(self):
        return Fanfic.objects.visible_to(self.request.user).with_related()

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            return FanficWriteSerializer
        if self.action == "retrieve":
            return FanficDetailSerializer
        return FanficListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        services.register_view(instance, request.session)
        return Response(self.get_serializer(instance).data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShareFanficAPIView(generics.GenericAPIView):
    """E-mail a published fanfic to a friend."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "share"
    serializer_class = ShareFanficSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.validated_data
        services.share_by_email(
            data["id"],
            name=data["name"],
            email=data["email"],
            to_email=data["to_email"],
            comments=data.get("comments", ""),
        )
        return Response({"message": "ok"})


class EmailFeedbackView(generics.GenericAPIView):
    """Report a fanfic to the moderators."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "feedback"
    serializer_class = FanficReferenceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        services.report_to_moderators(serializer.validated_data["id"])
        return Response({"message": "ok"})


class UserRecommendationsAPIView(generics.ListAPIView):
    """Fanfics recommended to the current user (consent required)."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FanficListSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Fanfic.objects.none()
        if not self.request.user.accountprofile.reco_consent_given:
            raise PermissionDenied("You must give consent to receive recommendations")
        return services.recommended_fanfics(self.request.user)

    def delete(self, request, *args, **kwargs):
        services.clear_recommendations(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
