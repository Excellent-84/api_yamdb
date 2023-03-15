from rest_framework import viewsets

from .serializers import UserSerializer
from .permissions import OwnerOrReadOnly
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (OwnerOrReadOnly,)

    def signup(self, requests):
        return requests

    def token(self, request):
        return request
