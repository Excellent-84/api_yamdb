from django.db import models


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
