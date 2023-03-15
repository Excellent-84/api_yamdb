from django.contrib import admin

from .models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'text',
        'author', 'score', 'pub_date',
    )
    search_fields = ('title', 'author', 'pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'review', 'text',
        'author', 'pub_date',
    )
    search_fields = ('author', 'review', 'pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
