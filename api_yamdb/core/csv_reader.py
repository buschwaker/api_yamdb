import csv

from reviews.models import Category, Comment, Genre, MyUser, Review, Title


def create_users():
    """
    Создание dummy data для пользователей из csv файла
    Запуск из shell:

    from core.csv_reader import create_users
    create_users()
    """
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
    """
    Создание фиктивных данных для модели жанра из csv файла.
    Запуск из shell:
    from core.csv_reader import create_genre
    create_genre()
    """
    with open('static/data/genre.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Genre.objects.create(
                id=row.get('id'),
                name=row.get('name'),
                slug=row.get('slug'),
            )


def create_categories():
    """
    Создание фиктивных данных для модели категории из csv файла.
    Запуск из shell:
    from core.csv_reader import create_categories
    create_categories()
    """
    with open('static/data/category.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Category.objects.create(
                id=row.get('id'),
                name=row.get('name'),
                slug=row.get('slug'),
            )


def create_titles():
    """
    Создание фиктивных данных для модели тайтла из csv файла.
    Запуск из shell:
    from core.csv_reader import create_titles
    create_titles()
    """
    with open('static/data/titles.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Title.objects.create(
                id=row.get('id'),
                name=row.get('name'),
                year=row.get('year'),
                category=Category.objects.filter(pk=row.get('category'))
            )


def create_reviews():
    """
    Создание фиктивных данных для модели отзыва из csv файла.
    Запуск из shell:
    from core.csv_reader import create_reviews
    create_reviews()
    """
    with open('static/data/review.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Review.objects.create(
                id=row.get('id'),
                title=Title.objects.filter(pk=row.get('title_id')),
                text=row.get('text'),
                author=MyUser.objects.filter(pk=row.get('author')),
                score=row.get('score'),
                pub_date=row.get('pub_date'),
            )


def create_comments():
    """
    Создание фиктивных данных для модели комментария из csv файла.
    Запуск из shell:
    from core.csv_reader import create_comments
    create_comments()
    """
    with open('static/data/comments.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Comment.objects.create(
                id=row.get('id'),
                review=Review.objects.filter(pk=row.get('review_id')),
                text=row.get('text'),
                author=MyUser.objects.filter(pk=row.get('author')),
                pub_date=row.get('pub_date'),
            )
