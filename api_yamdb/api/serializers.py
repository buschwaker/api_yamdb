from django.db.models import Avg
from rest_framework import serializers
from rest_framework import exceptions

from reviews.models import Category, Genre, MyUser, Title


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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        

class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        return reviews.aggregate(Avg('score'))['score__avg']


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
