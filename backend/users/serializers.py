from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField

User = get_user_model()


class MyUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):  # todo
        return False

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed',
            'avatar',
        )


class AvatarSerializer(ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar',)

    def validate_avatar(self, value):
        if not value:
            raise ValidationError('Передано пустое поле avatar.')
        return value
