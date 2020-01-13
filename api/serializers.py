from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from fanfics.models import Fanfic
from chapters.models import Chapter

from api.models import FlatPages
from api.models import Notification

from django.contrib.contenttypes.models import ContentType


class FlatPagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlatPages
        fields = (
            'id',
            'title',
            'content',
            'type',
            'created',
            'updated'
        )

"""
Serializer for password change endpoint
"""
class ChangePasswordSerializer(serializers.Serializer):


    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


"""
Notification serializer
"""

class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = '__all__'


class NotificationObjectRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, User):
            return value.username
        elif isinstance(value, Chapter):
            return value.title
        elif isinstance(value, Fanfic):
            return value.title
        raise Exception('Unexpected type of object')


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    target = NotificationObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = (
            'id',
            'user',
            'verb',
            'target_ct',
            'target_id',
            'target',
            'created',
        )

    def get_target_ct(self, obj):
        return Fanfic.objects.all()
