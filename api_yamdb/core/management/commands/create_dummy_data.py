from django.core.management.base import BaseCommand
from core.csv_reader import main


class Command(BaseCommand):

    help = 'Команда создающая dummy data'

    def handle(self, *args, **kwargs):
        main()
