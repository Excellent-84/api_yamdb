from rest_framework import serializers

from api.validators import validate_username
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


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, max_length=150,  validators=(validate_username,)
    )

    email = serializers.EmailField(
        required=True, max_length=254
    )

    class Meta:
        model = User
        fields = ('email', 'username')
