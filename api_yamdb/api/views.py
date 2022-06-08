from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import MyUser, Review, Title, Category, Genre
from api import permissions, serializers
from api.mixins import CreateDestroyListViewSet
from api.filters import TitleFilter
from core.key_generator import generate_alphanum_random_string


class SignUpView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        code = generate_alphanum_random_string(16)
        username = request.data.get('username')
        email = request.data.get('email')
        try:
            user = get_object_or_404(MyUser, username=username, email=email)
        except Http404:
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


class GetToken(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = MyUser.objects.get(
                username=request.data.get('username'),
                confirmation_code=request.data.get('confirmation_code')
            )
            refresh = RefreshToken.for_user(user)
            user.confirmation_code = ''
            user.save()
            return Response({'token': str(refresh.access_token), })
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс представления отзывов."""
    serializer_class = serializers.ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        permissions.IsAuthorModeratorAdmin,
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс представления комментария к отзывам."""
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        permissions.IsAuthorModeratorAdmin,
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleReadSerializer
        return serializers.TitleCreateSerializer


class CategoryViewSet(CreateDestroyListViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
