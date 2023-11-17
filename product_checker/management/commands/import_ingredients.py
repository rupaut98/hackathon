import csv
from django.core.management.base import BaseCommand
from product_checker.models import Ingredient

class Command(BaseCommand):
    help = 'Loads a list of ingredients from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to load')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Ingredient.objects.create(
                    name=row['ingredient'],
                    description=row['description'],
                    country_banned_in=row['country_banned_in'],
                    severity=row['severity'],
                    is_unhealthy=True  # Set to True for all records
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded ingredients from CSV'))
