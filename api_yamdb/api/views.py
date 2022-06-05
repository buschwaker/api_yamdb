from api import permissions, serializers
from core.key_generator import generate_alphanum_random_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import MyUser, Review, Title


class SignUpView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        code = generate_alphanum_random_string(16)
        username = request.data.get('username')
        email = request.data.get('email')
        try:
            user = MyUser.objects.get(username=username, email=email)
        except MyUser.DoesNotExist:
            serializer = serializers.SignUpSerializer(data=request.data)
            if serializer.is_valid():
                user = MyUser.objects.create_user(
                    username=username,
                    email=email
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        user.confirmation_code = code
        user.save()
        send_mail(
            'Ваш код подтверждения',
            f'{code}',
            'akroshko1995@gmail.com',
            [f'{email}'],
            fail_silently=True
        )
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    # lookup_value_regex = '[\w.@+-]+ '
    lookup_value_regex = '(?!me).*'
    queryset = MyUser.objects.all()
    permission_classes = [permissions.IsAdmin, ]

    def get_serializer_class(self):
        if self.action == 'me':
            return serializers.MeSerializer
        return serializers.UserSerializer

    @action(
        detail=False, url_name='me',
        methods=['get', 'patch'], permission_classes=[IsAuthenticated, ]
    )
    def me(self, request):
        me = MyUser.objects.get(username=request.user.username)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                me,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(me)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_tokens_for_user(request):
    serializer = serializers.TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = MyUser.objects.get(
            username=request.data.get('username'),
            confirmation_code=request.data.get('confirmation_code')
        )
        refresh = RefreshToken.for_user(user)
        user.confirmation_code = ''
        user.save()
        return Response({'access': str(refresh.access_token), })
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


class ReviewView(viewsets.ModelViewSet):
    """Класс представления отзывов."""
    serializer = serializers.ReviewSerializer
    permission_classes = [
        permissions.IsAuthor,
        permissions.IsModerator,
        permissions.IsAdmin,
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentView(viewsets.ModelViewSet):
    """Класс представления комментария к отзывам."""
    serializer = serializers.CommentSerializer
    permission_classes = [
        permissions.IsAuthor,
        permissions.IsModerator,
        permissions.IsAdmin,
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
