import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    email = models.EmailField(_('email address'), blank=False, null=False, max_length=254)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    bio = models.TextField(blank=True)

    anon = 'anon'
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    ROLE_CHOICES = [
        (anon, 'Anonymous User'),
        (user, 'Authenticated User'),
        (moderator, 'Moderator'),
        (admin, 'Administrator'),
    ]

    role = models.CharField(choices=ROLE_CHOICES, default=user, max_length=9)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_staff is True:
            self.role = self.admin
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField('Категория', max_length=255)
    slug = models.SlugField('Slug категории', max_length=50, unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=255)
    slug = models.SlugField('Slug жанра', max_length=50, unique=True)

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=255)
    year = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(datetime.date.today().year)],
        help_text='Используйте формат: <ГГГГ>',
        verbose_name='Год создания'
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True,
        verbose_name='Жанр произведения',
        related_name='genre'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='category'
    )
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name
