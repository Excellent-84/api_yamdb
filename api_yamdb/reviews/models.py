from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    """Отзывы пользователей."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рецензируемое произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(
        'Оценка (от 1 до 10)',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        constrains = (
            models.UniqueConstraint(
                fields=['title', 'author'], name='title_one_review'
            ),
        )
        ordering = ('title',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к отзывам."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв'
    )
    text = models.TextField(
        max_length=2000,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания комментария'
    )

    class Meta:
        ordering = ('review', 'author')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

class Category(models.Model):
    name = models.CharField('Имя', max_length=200)
    slug = models.SlugField('Слаг', unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Имя', max_length=200)
    slug = models.SlugField('Слаг', unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Имя', max_length=200)
    year = models.PositiveSmallIntegerField('Год')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle', related_name='titles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='titles')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='genre_title')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genre_title')

    class Meta:
        unique_together = ('title', 'genre')

    def __str__(self):
        return self.title.name + ' - ' + self.genre.name
