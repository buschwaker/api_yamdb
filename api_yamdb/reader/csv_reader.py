import csv

from reviews.models import MyUser


def create_users():
    """
    Создание dummy data для пользователей из csv файла
    Запуск из shell:

    from reader.csv_reader import create_users
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
