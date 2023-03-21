import uuid
from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import IsAdmin
from .serializers import SignUpSerializers, TokenSerializers, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        ['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    confirmation_code = str(uuid.uuid4())
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail(
            'Код подтверждения регистрации',
            confirmation_code,
            settings.EMAIL_HOST,
            [serializer.data['email']]
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
    user = get_object_or_404(User, username=username)
    serializer = SignUpSerializers(
        user, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['email'] == user.email:
        serializer.save(role=user.role)
        send_mail(
            'Код подтверждения регистрации',
            confirmation_code,
            settings.EMAIL_HOST,
            [serializer.data['email']]
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
    return Response(
        'Ошибка обязательного поля',
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
    except User.DoesNotExist:
        return Response(
            'Пользователь не найден', status=status.HTTP_404_NOT_FOUND
        )
    if (serializer.validated_data['confirmation_code']
       == user.confirmation_code):
        token = default_token_generator.make_token(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_201_CREATED
        )
    return Response(
        'Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST
    )
