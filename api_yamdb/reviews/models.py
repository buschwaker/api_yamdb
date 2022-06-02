from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        blank=False,
        null=False,
        max_length=254,
        unique=True
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    bio = models.TextField(blank=True)
    confirmation_code = models.TextField(blank=True)

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
