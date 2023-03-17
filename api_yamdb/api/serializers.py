import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Review, Comment, Category, Genre, Title


class ReviewCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=False
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    score = serializers.IntegerField(max_value=10, min_value=1)

    def validate(self, data):
        request = self.context.get('request')

        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(
            author=request.user, title=title
        ).exists():
            raise serializers.ValidationError(
                'Ваш отзыв уже есть!'
            )
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
        read_only = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'
