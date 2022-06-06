import csv

from reviews.models import MyUser, Title, Category, Genre, Review, Comment


def create_users():
    """Создание dummy data для пользователей из csv файла"""
    with open('static/data/users.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            MyUser.objects.create(
                id=row.get('id'),
                username=row.get('username'),
                email=row.get('email'),
                role=row.get('role')
            )


def create_genre():
    """Создание dummy data для жанров из csv файла"""
    with open('static/data/genre.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Genre.objects.create(
                id=row.get('id'),
                name=row.get('name'),
                slug=row.get('slug'),
            )


def create_categories():
    """Создание dummy data для категорий из csv файла"""
    with open('static/data/category.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Category.objects.create(
                id=row.get('id'),
                name=row.get('name'),
                slug=row.get('slug'),
            )


def create_titles():
    """Создание dummy data для произведений из csv файла"""
    with open('static/data/titles.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Title.objects.create(
                id=row.get('id'),
                name=row.get('name'),
                year=row.get('year'),
                category=Category.objects.get(pk=row.get('category'))
            )


def create_review():
    """Создание dummy data для отзывов из csv файла"""
    with open('static/data/review.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Review.objects.create(
                id=row.get('id'),
                title=Title.objects.get(pk=row.get('title_id')),
                text=row.get('text'),
                author=MyUser.objects.get(pk=row.get('author')),
                score=row.get('score'),
                pub_date=row.get('pub_date')
            )


def create_comment():
    """Создание dummy data для комментариев из csv файла"""
    with open('static/data/comments.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Comment.objects.create(
                id=row.get('id'),
                review=Review.objects.get(pk=row.get('review_id')),
                text=row.get('text'),
                author=MyUser.objects.get(pk=row.get('author')),
                pub_date=row.get('pub_date')
            )


def main():
    create_users()
    create_categories()
    create_genre()
    create_titles()
    create_review()
    create_comment()
