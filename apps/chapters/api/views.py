from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from apps.chapters import services
from apps.chapters.api.serializers import (
    ChapterAutosaveSerializer,
    ChapterFormattedSerializer,
    ChapterSerializer,
    ChapterSummaryRequestSerializer,
    ChapterSummaryResponseSerializer,
)
from apps.chapters.models import Chapter
from apps.core.permissions import IsOwnerOrReadOnly
from apps.fanfics.models import Fanfic


def _as_drf_error(exc: DjangoValidationError) -> ValidationError:
    return ValidationError(
        exc.message_dict if hasattr(exc, "error_dict") else {"detail": exc.messages}
    )


class ChapterListApiView(generics.ListAPIView):
    """Chapters of a fanfic, in reading order (drafts only for their author)."""

    serializer_class = ChapterFormattedSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["status"]
    ordering_fields = ["order", "created", "published"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Chapter.objects.none()
        fanfic_id = self.kwargs.get("fanfic") or self.request.query_params.get("fanfic")
        if not fanfic_id:
            raise NotFound("No fanfic id provided")
        return (
            Chapter.objects.visible_to(self.request.user)
            .filter(fanfic_id=fanfic_id)
            .select_related("author", "fanfic")
            .order_by("order")
        )


class ChapterCreateApiView(generics.CreateAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except DjangoValidationError as exc:
            raise _as_drf_error(exc) from exc


class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Chapter.objects.visible_to(self.request.user).select_related("author")

    def perform_update(self, serializer):
        try:
            serializer.save()
        except DjangoValidationError as exc:
            raise _as_drf_error(exc) from exc


class SummaryStylesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="List all styles prompts",
        responses={200: OpenApiResponse(description="List of styles")},
        tags=["Chapters"],
    )
    def get(self, request):
        return Response(services.SUMMARY_STYLES)


class GenerateSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Generate chapter summary",
        request=ChapterSummaryRequestSerializer,
        responses={200: ChapterSummaryResponseSerializer},
        tags=["Chapters"],
    )
    def post(self, request):
        serializer = ChapterSummaryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            summary = services.generate_summary(**serializer.validated_data)
        except services.SummaryGenerationError:
            return Response(
                {"error": "La génération du résumé a échoué."},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response({"generated_summary": summary})


class AutosaveChapterView(APIView):
    """Save a draft chapter of one of the user's fanfics."""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Autosave a chapter",
        request=ChapterAutosaveSerializer,
        responses={200: OpenApiResponse(description="Autosaved draft")},
        tags=["Chapters"],
    )
    def post(self, request, fanfic):
        fanfic = get_object_or_404(Fanfic, pk=fanfic, author=request.user)
        serializer = ChapterAutosaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        chapter_id = data.pop("id", None)
        try:
            chapter, created = services.autosave(
                fanfic=fanfic, author=request.user, data=data, chapter_id=chapter_id
            )
        except Chapter.DoesNotExist as exc:
            raise NotFound("Chapter not found") from exc
        except DjangoValidationError as exc:
            raise _as_drf_error(exc) from exc
        return Response(
            {
                "message": "Autosaved",
                "id": chapter.id,
                "created": created,
                "updated": chapter.updated,
                "published": chapter.published,
                "is_published": chapter.is_published,
                "fanfic": fanfic.title,
                "title": chapter.title,
                "description": chapter.description,
                "text": chapter.text,
                "order": chapter.order,
                "status": chapter.status,
                "author": request.user.username,
                "fanfic_id": fanfic.id,
                "author_id": request.user.id,
            }
        )
