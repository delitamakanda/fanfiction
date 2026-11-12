from rest_framework import serializers

from apps.posts.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("word",)
        read_only_fields = fields


class PostSerializer(serializers.ModelSerializer):
    username_author = serializers.CharField(source="user.username", read_only=True)
    email_author = serializers.CharField(source="user.email", read_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=35), required=False, write_only=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "username_author",
            "email_author",
            "header",
            "title",
            "slug",
            "content",
            "created",
            "tags",
            "category",
        )
        read_only_fields = ("id", "slug", "created")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tags"] = [tag.word for tag in instance.tags.all()]
        return data

    def _set_tags(self, post, words):
        if words is None:
            return
        tags = [
            Tag.objects.get_or_create(word=word.strip())[0]
            for word in words
            if word.strip()
        ]
        post.tags.set(tags)

    def create(self, validated_data):
        words = validated_data.pop("tags", None)
        post = super().create(validated_data)
        self._set_tags(post, words)
        return post

    def update(self, instance, validated_data):
        words = validated_data.pop("tags", None)
        post = super().update(instance, validated_data)
        self._set_tags(post, words)
        return post
