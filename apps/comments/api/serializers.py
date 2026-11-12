from rest_framework import serializers

from apps.chapters.models import Chapter
from apps.comments.models import Comment
from apps.fanfics.models import Fanfic


class CommentNestedSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "body", "created")
        read_only_fields = fields


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    fanfic = serializers.PrimaryKeyRelatedField(queryset=Fanfic.published.all())
    chapter = serializers.PrimaryKeyRelatedField(
        queryset=Chapter.objects.published(), required=False, allow_null=True
    )
    in_reply_to = CommentNestedSerializer(read_only=True)
    in_reply_to_id = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.filter(active=True),
        source="in_reply_to",
        write_only=True,
        required=False,
        allow_null=True,
    )
    fanfic_title = serializers.CharField(source="fanfic.title", read_only=True)
    chapter_title = serializers.CharField(
        source="chapter.title", read_only=True, default=None
    )
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "fanfic",
            "chapter",
            "body",
            "created",
            "updated",
            "active",
            "in_reply_to",
            "in_reply_to_id",
            "fanfic_title",
            "chapter_title",
            "is_author",
        )
        read_only_fields = ("id", "author", "created", "updated", "active")

    def get_is_author(self, obj) -> bool:
        request = self.context.get("request")
        return bool(
            request
            and request.user.is_authenticated
            and obj.author_id == request.user.pk
        )

    def validate_body(self, value):
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError(
                "Comment body must be at least 5 characters long"
            )
        if len(value) > 5000:
            raise serializers.ValidationError(
                "Comment body cannot exceed 5000 characters"
            )
        return value

    def validate(self, attrs):
        fanfic = attrs.get("fanfic", getattr(self.instance, "fanfic", None))
        chapter = attrs.get("chapter")
        reply_to = attrs.get("in_reply_to")
        if (
            self.instance is not None
            and "fanfic" in attrs
            and attrs["fanfic"] != self.instance.fanfic
        ):
            raise serializers.ValidationError(
                {"fanfic": "A comment cannot change fanfic."}
            )
        if chapter is not None and chapter.fanfic_id != fanfic.pk:
            raise serializers.ValidationError(
                {"chapter": "This chapter does not belong to the fanfic."}
            )
        if reply_to is not None and reply_to.fanfic_id != fanfic.pk:
            raise serializers.ValidationError(
                {"in_reply_to_id": "Invalid reply to comment ID"}
            )
        return attrs
