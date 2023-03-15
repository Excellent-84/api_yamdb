from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Уже подписан на этого пользователя'
            )
        ]

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать логин "me" запрещено'
            )
        return username
