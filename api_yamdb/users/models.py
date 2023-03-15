from django.contrib.auth.models import AbstractUser
from django.db import models


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
        'Логин', max_length=150, unique=True
    )
    email = models.EmailField(
        'Почта', max_length=254, unique=True
    )
    first_name = models.CharField(
        'Имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True
    )
    bio = models.TextField(
        'Биография', blank=True
    )
    role = models.CharField(
        'Роль', max_length=20, choices=ROLE_CHOICES, default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=50, blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [models.UniqueConstraint(
            fields=['username', 'email'], name='unigue_together')
        ]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username
