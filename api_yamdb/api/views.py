from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, MyUser, Title
from api import serializers
from core.key_generator import generate_alphanum_random_string
from api import permissions


class CreateDestroyListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleReadSerializer
        return serializers.TitleCreateSerializer


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAdminOrReadOnly, ]
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
