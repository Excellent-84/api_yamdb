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


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=150, validators=(validate_username,)
    )

    email = serializers.EmailField(
        required=True, max_length=254
    )


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
        if self.context.get('request').method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            user = self.context['request'].user
            if not Review.objects.filter(title_id=title_id,
                                         author=user).exists():
                return data
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
