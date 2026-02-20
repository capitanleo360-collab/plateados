from django.core.management.base import BaseCommand
from core.models import Category

class Command (BaseCommand):

    help = 'sembrar datos iniciales en la base de datos Categorias'

    def handle(self, *args, **options):
        self.seed_categories()
    def seed_categories (self):

        categories = [
            {'name':'desayuno', 'description':'comidas de 7-10 am'},
            {'name':'almuerzo', 'description':'11-1 pm'},
            {'name':'postres', 'description':'3-5 pm'},
            {'name':'cena', 'description':'6-9 pm'},

        ]

        for category in categories:
            category, created = Category.objects.get_or_create(defaults=category,name=category['name'],description=category['description'])

            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoria "{category.name}" creada.'))
            else:
                self.stdout.write(self.style.WARNING(f'Categoria "{category.name}" ha sido actualizada.'))
