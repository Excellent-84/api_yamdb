from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleGetSerializer, TitlePostSerializer


class CategoryViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitlePostSerializer
    queryset = (
        Title.objects.all()
        # .annotate(rating=Avg("reviews__score"))
        # .order_by('-year', 'name')
    )
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer
