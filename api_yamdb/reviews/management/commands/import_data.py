from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
from reviews.models import Comment, Review, Category, Genre, Title, GenreTitle
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for row in DictReader(
                open('./static/data/users.csv')
        ):
            user = User(
                id=row['id'], username=row['username'],
                email=row['email'], role=row['role'],
                bio=row['bio'], first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()
        for row in DictReader(
                open('./static/data/category.csv')
        ):
            category = Category(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            category.save()
        for row in DictReader(
                open('./static/data/genre.csv')
        ):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()
        for row in DictReader(
                open('./static/data/titles.csv')
        ):
            title = Title(
                id=row['id'], name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category'])

            )
            title.save()
        for row in DictReader(
                open('./static/data/genre_title.csv')
        ):
            genretitle = GenreTitle(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                genre=Genre.objects.get(id=row['genre_id'])
            )
        genretitle.save()
        for row in DictReader(
                open('./static/data/review.csv')
        ):
            pub_date_str = row['pub_date']
            pub_date = datetime.strptime(
                pub_date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
            review = Review(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'], author=User.objects.get(id=row['author']),
                score=row['score'], pub_date=pub_date
            )

            review.save()
        for row in DictReader(
                open('./static/data/comments.csv')
        ):
            comment = Comment(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date']
            )

            comment.save()
