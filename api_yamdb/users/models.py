from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import validate_username


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        'Логин', max_length=150, unique=True, validators=(validate_username,)
    )
    email = models.EmailField(
        'Почта', max_length=254, unique=True
    )
    bio = models.TextField(
        'Биография', blank=True
    )
    role = models.CharField(
        'Роль', max_length=20, choices=ROLE_CHOICES, default=USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=50, blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    def __str__(self):
        return self.username
