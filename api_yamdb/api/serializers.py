import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')


class ReviewCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=False
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(
                title=get_object_or_404(
                    Title,
                    id=self.context['view'].kwargs.get('title_id')
                ),
                author=self.context['request'].user
            ).exists():
                raise serializers.ValidationError("Ваш отзыв уже есть!")
        return data

    def validate_year(self, value):
        year = datetime.now().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
