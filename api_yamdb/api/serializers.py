from rest_framework import exceptions, serializers
from reviews.models import Comment, MyUser, Review


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


class ReviewSerializer(serializers.Serializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault,
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        review = Review.objects.filter(title=title, author=author)
        if review.exists():
            raise serializers.ValidationError('Вы уже оставляли отзыв.')
        return data

    def validate_score(self, score):
        if 1 <= score <= 10:
            return score
        raise serializers.ValidationError('Оценка должна быть от 1 до 10.')


class CommentSerializer(serializers.Serializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault,
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
