from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Category, Genre, MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'bio')}),
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
