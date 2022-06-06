from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'


# у нас ни о кого нет PUT запросов, предлагаю регистрировать этот роутер
class NoPutRouter(routers.DefaultRouter):
    """
    Класс роутер, отключающий PUT запросы
    """
    def get_method_map(self, viewset, method_map):

        bound_methods = super().get_method_map(viewset, method_map)

        if 'put' in bound_methods.keys():
            del bound_methods['put']

        return bound_methods


router_v1 = NoPutRouter()

# Здесь подключаем ресурсы
router_v1.register('users', views.UserViewSet, basename='user')

router_v1.register(
    r'titles/?P<title_id>[0-9]+/reviews/',
    views.ReviewView,
    basename='review',
)
router_v1.register(
    r'titles/?P<title_id>[0-9]+/reviews/?P<review_id>[0-9]+/comments/',
    views.CommentView,
    basename='comment',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.SignUpView.as_view()),
    path('v1/auth/token/', views.GetToken.as_view()),
]
