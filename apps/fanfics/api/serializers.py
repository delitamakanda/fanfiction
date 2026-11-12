from rest_framework import serializers

from apps.fanfics.models import Fanfic


class GenresField(serializers.MultipleChoiceField):
    """Genres as a JSON list of codes, e.g. ``["RO", "DR"]``."""

    def __init__(self, **kwargs):
        super().__init__(choices=Fanfic.GENRES_CHOICES, **kwargs)

    def to_representation(self, value):
        return [code for code in value if code in self.choices]

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = [code for code in data.split(",") if code]
        return sorted(super().to_internal_value(data))


class FanficListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fanfic
        fields = [
            "id",
            "slug",
            "category",
            "subcategory",
            "title",
            "synopsis",
            "author",
            "total_likes",
            "views",
            "created",
        ]
        read_only_fields = fields


class FanficDetailSerializer(serializers.ModelSerializer):
    genres = GenresField(read_only=True)

    class Meta:
        model = Fanfic
        fields = [
            "id",
            "title",
            "slug",
            "synopsis",
            "credits",
            "picture",
            "language",
            "description",
            "classement",
            "genres",
            "publish",
            "created",
            "updated",
            "was_featured_in_home",
            "status",
            "total_likes",
            "completed",
            "views",
            "fanfic_is_scraped",
            "link_fanfic",
            "author",
            "category",
            "subcategory",
            "users_like",
        ]
        read_only_fields = fields


class FanficWriteSerializer(serializers.ModelSerializer):
    """Create / update a fanfic. The author is always the current user."""

    genres = GenresField(allow_empty=False)

    class Meta:
        model = Fanfic
        fields = [
            "id",
            "slug",
            "title",
            "synopsis",
            "description",
            "credits",
            "genres",
            "classement",
            "category",
            "subcategory",
            "language",
            "picture",
            "status",
            "completed",
        ]
        read_only_fields = ["id", "slug"]

    def validate(self, attrs):
        category = attrs.get("category", getattr(self.instance, "category", None))
        subcategory = attrs.get(
            "subcategory", getattr(self.instance, "subcategory", None)
        )
        if category and subcategory and subcategory.category_id != category.pk:
            raise serializers.ValidationError(
                {"subcategory": "Cette sous-catégorie n'appartient pas à la catégorie."}
            )
        return attrs


class ChoiceSerializer(serializers.Serializer):
    id = serializers.CharField()
    libelle = serializers.CharField()


class FanficLikeSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Fanfic.published.all())
    action = serializers.ChoiceField(choices=["like", "unlike"])


class FanficReferenceSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Fanfic.published.all())


class ShareFanficSerializer(FanficReferenceSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    to_email = serializers.EmailField()
    comments = serializers.CharField(max_length=2000, required=False, allow_blank=True)
