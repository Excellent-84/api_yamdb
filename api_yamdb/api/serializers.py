from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb.settings import MIN_VALUE_SCORE, MAX_VALUE_SCORE
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_username
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(required=True)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=(validate_username,)
    )
    email = serializers.EmailField(
        max_length=254
    )


class MeUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = fields


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
    )
    score = serializers.IntegerField(max_value=MAX_VALUE_SCORE,
                                     min_value=MIN_VALUE_SCORE)

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        if Review.objects.filter(
            title=get_object_or_404(
                Title,
                id=self.context['view'].kwargs.get('title_id')),
                author=self.context['request'].user).exists():
            raise serializers.ValidationError('Ваш отзыв уже есть!')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
