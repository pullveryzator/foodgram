"""Import csv files to database."""
import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

data_files = {
    'ingredient': 'data/ingredients.csv',
}


class Command(BaseCommand):
    """Command for import csv into database."""

    help = 'Import csv files to database.'

    def handle(self, *args, **options):
        """Handle function."""
        for model, file_path in data_files.items():
            print(f'Importing {file_path} to {model}...')
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    obj = self.create_object(model, row)
                    if obj:
                        obj.save()
            print(f'Success import {file_path}.')

    def create_object(self, model_name, data):
        """Create object from django ORM."""
        if model_name == 'ingredient':
            return Ingredient(**data)
