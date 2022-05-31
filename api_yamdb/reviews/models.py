from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    email = models.EmailField(
        _('email address'), blank=False, null=False, max_length=254)
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


class Review(MyUser):
    """Модель отзыва."""
    text = models.TextField(_('text'))
    score = models.IntegerField(
        _('score'),
        validators=[
            MinValueValidator(1, 'Минимальная оценка: 1'),
            MaxValueValidator(10, 'Максимальная оценка: 10')
        ]
    )
    title = models.ForeignKey(_('title'), Title, on_delete=models.CASCADE)
    author = models.ForeignKey(_('author'), MyUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        _('publishing date'), auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:10]

    class Meta:
        # Устаревший вариант, думаю не стоит юзать.
        # unique_together = ('author', 'title')

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        ordering = ['-pub_date']


class Comment(MyUser):
    """Модель комментария."""
    review = models.ForeignKey(
        _('review'), Review, on_delete=models.CASCADE, related_name='comments')
    title = models.ForeignKey(_('title'), Title, on_delete=models.CASCADE)
    text = models.TextField(_('text'))
    author = models.ForeignKey(_('author'), MyUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        _('publishing date'), auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:10]
