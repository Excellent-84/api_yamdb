from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)

from api_yamdb.settings import LENG_CUT, LENG_MAX
from users.models import User


def validate_year(value):
    year = datetime.now().year
    if value > year:
        raise ValidationError('Проверьте год выпуска!')
    return value


class Category(models.Model):
    name = models.CharField('Имя', max_length=256)
    slug = models.SlugField('Слаг', unique=True, max_length=50, validators=[
        RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Недопустимые символы'),
    ], )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Имя', max_length=256)
    slug = models.SlugField('Слаг', unique=True, max_length=50, validators=[
        RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Недопустимые символы'),
    ], )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Имя', max_length=256)
    year = models.PositiveSmallIntegerField('Год', validators=[validate_year])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre_titles'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_titles'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_genre_title')
        ]

    def __str__(self):
        return f'{self.title} - {self.genre}'


class ReviewAndCommentModel(models.Model):
    """Модель для наследования."""

    text = models.CharField(
        max_length=LENG_MAX
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LENG_CUT]


class Review(ReviewAndCommentModel):
    """Отзывы пользователей."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рецензируемое произведение'
    )
    score = models.IntegerField(
        'Оценка (от 1 до 10)',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    class Meta(ReviewAndCommentModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:LENG_CUT]


class Comment(ReviewAndCommentModel):
    """Комментарии к отзывам."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв'
    )

    class Meta(ReviewAndCommentModel.Meta):
        ordering = ('review', 'author')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LENG_CUT]
