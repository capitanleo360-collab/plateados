from django.core.management.base import BaseCommand
from core.models import Category

class Command (BaseCommand):

    help = 'sembrar datos iniciales en la base de datos Categorias'

    def handle(self, *args, **options):
        self.seed_categories()
    def seed_categories (self):

        categories = [
            {'name':'desayuno', 'description':'nicolas maduro 3.4'},
            {'name':'almuerzo', 'description':'diosdado sin cabello'}
        ]

        for category in categories:
            category, created = Category.objects.update_or_create(defaults=category,name=category['name'],description=category['description'])

            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoria "{category.name}" creada.'))
            else:
                self.stdout.write(self.style.WARNING(f'Categoria "{category.name}" ha sido actualizada.'))
