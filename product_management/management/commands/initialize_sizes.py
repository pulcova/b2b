from django.core.management.base import BaseCommand
from product_management.models import Size  # Replace 'your_app' with your Django app's name

class Command(BaseCommand):
    help = 'Create initial sizes'

    def handle(self, *args, **options):
        sizes = [
            'S',
            'M',
            'L',
            'XL',
            # Add more sizes as needed
        ]

        for name in sizes:
            size, created = Size.objects.get_or_create(
                name=name
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Size created: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Size already exists: {name}'))