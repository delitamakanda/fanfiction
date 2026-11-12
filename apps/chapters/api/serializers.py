from rest_framework import serializers

from apps.chapters.models import Chapter
from apps.chapters.services import SUMMARY_STYLES
from apps.fanfics.models import Fanfic


class ChapterFormattedSerializer(serializers.ModelSerializer):
    """Compact representation used in chapter lists."""

    status = serializers.CharField(source="get_status_display", read_only=True)
    author = serializers.CharField(source="author.username", read_only=True)
    fanfic = serializers.CharField(source="fanfic.title", read_only=True)

    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "description",
            "order",
            "status",
            "author",
            "fanfic",
            "created",
            "updated",
            "published",
        ]
        read_only_fields = fields


class ChapterSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    fanfic_id = serializers.PrimaryKeyRelatedField(
        queryset=Fanfic.objects.all(), source="fanfic", write_only=True
    )
    is_published = serializers.BooleanField(read_only=True)

    class Meta:
        model = Chapter
        fields = (
            "id",
            "title",
            "description",
            "text",
            "order",
            "status",
            "author",
            "fanfic_id",
            "created",
            "updated",
            "published",
            "is_published",
        )
        read_only_fields = ("id", "created", "updated", "author", "order", "published")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields["fanfic_id"].required = False

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required and cannot be empty")
        return value.strip()

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Text is required and cannot be empty")
        return value.strip()

    def validate_fanfic_id(self, fanfic):
        if self.instance is not None and fanfic.pk != self.instance.fanfic_id:
            raise serializers.ValidationError("A chapter cannot change fanfic.")
        if fanfic.author_id != self.context["request"].user.pk:
            raise serializers.ValidationError(
                "You are not authorized to create chapters for this fanfic"
            )
        return fanfic


class ChapterAutosaveSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, help_text="Draft to update")
    title = serializers.CharField(required=False, allow_blank=True, max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    text = serializers.CharField(required=False, allow_blank=True)
    order = serializers.IntegerField(required=False, min_value=0)


class ChapterSummaryRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(
        max_length=4000, help_text="The prompt for the chapter summary"
    )
    style = serializers.ChoiceField(
        choices=SUMMARY_STYLES,
        default="neutre",
        help_text="The style of the chapter summary",
    )


class ChapterSummaryResponseSerializer(serializers.Serializer):
    generated_summary = serializers.CharField()
