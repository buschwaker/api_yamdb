from rest_framework import serializers
from rest_framework import exceptions

from reviews.models import MyUser


class SignUpSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Нельзя называться 'me'")
        return value

    class Meta:
        model = MyUser
        fields = ('username', 'email')


class UserSerializer(SignUpSerializer):

    class Meta(SignUpSerializer.Meta):
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class MeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role', )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        if not MyUser.objects.filter(username=attrs.get('username')).exists():
            raise exceptions.NotFound("Нет пользователя с таким именем")
        elif MyUser.objects.filter(
                username=attrs.get('username'),
                confirmation_code=attrs.get('confirmation_code')
        ).exists() and (
                attrs.get('confirmation_code') != ''
                or attrs.get('confirmation_code') is not None
        ):
            return attrs
        raise exceptions.ParseError("Невалидный код!")
