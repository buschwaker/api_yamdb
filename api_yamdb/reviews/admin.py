from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Category, Comment, Genre, MyUser, Review, Title


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    """Панель администратора для модели MyUser"""
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        (_('Personal info'),
         {'fields': (
             'first_name', 'last_name', 'email', 'bio', 'confirmation_code'
         )}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'role')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Управление жанрами админом."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
    )
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Управление категориями админом."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
    )
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Страница отзывов."""
    list_display = ('pk', 'pub_date', 'title', 'score', 'author', 'text')
    search_fields = ('title', 'author', 'text')
    list_filter = ('pub_date', 'title', 'score', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Страница комментариев."""
    list_display = ('pk', 'pub_date', 'review', 'author', 'text')
    search_fields = ('author', 'text')
    list_filter = ('pub_date', 'review', 'author')


admin.site.register(Title)
