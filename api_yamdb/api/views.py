from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (ListModelMixin, CreateModelMixin,
                                   DestroyModelMixin)

from .permissions import IsAuthorOrModerOrAdmin, IsAdminOrReadOnly
from .serializers import (ReviewCreateSerializer, CommentSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleGetSerializer, TitlePostSerializer)
from .filter import TitleFilter

from reviews.models import Review, Category, Comment, Genre, Title


class CategoryViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = (
        Title.objects.all()
        .annotate(rating=Avg("reviews__score"))
        .order_by('-year', 'name')
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCreateSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,)

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'),
        )

    def get_queryset(self):
        title = self.get_title()
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerOrAdmin,)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        review = self.get_review()
        queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )
