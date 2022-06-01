from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Comment, MyUser, Review


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
