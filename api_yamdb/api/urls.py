from django.urls import include, path
from rest_framework import routers

from api import views

app_name = 'api'


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

router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    views.ReviewViewSet,
    basename='review',
)
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    views.CommentViewSet,
    basename='comment',
)
router_v1.register('users', views.UserViewSet, basename='user')
router_v1.register('titles', views.TitleViewSet, basename='title')
router_v1.register('categories', views.CategoryViewSet, basename='category')
router_v1.register('genres', views.GenreViewSet, basename='genre')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.SignUpView.as_view()),
    path('v1/auth/token/', views.GetToken.as_view()),
]
