import uuid

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import SignUpSerializers, TokenSerializers, UserSerializer
from .permissions import OwnerOrReadOnly
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


@api_view(['POST'])
def signup(requests):
    serializer = SignUpSerializers(data=requests.data)
    confirmation_code = str(uuid.uuid4())
    if serializer.is_valid():
        serializer.save(
            username=serializer.validated_data['username'],
            confirmation_code=confirmation_code
        )
        send_mail(
            f'{confirmation_code} yamdb@yamdb.ru',
            [serializer.data['email']]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = get_object_or_404(
                User, username=serializer.validated_data['username']
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (serializer.validated_data['confirmation_code'] == user.confirmation_code):
            token = default_token_generator.make_token(request.user)
            return Response(
                {'token': str(token)}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
