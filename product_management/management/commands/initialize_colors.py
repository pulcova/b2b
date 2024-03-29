from django.core.management.base import BaseCommand
from product_management.models import Color  

class Command(BaseCommand):
    help = 'Create initial colors'

    def handle(self, *args, **options):
        colors = [
            ('Red', '#FF0000'),
            ('Green', '#008000'),
            ('Blue', '#0000FF'),
            # Add more colors as needed
        ]

        for name, hex_code in colors:
            color, created = Color.objects.get_or_create(
                name=name, 
                defaults={'hex_code': hex_code}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Color created: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Color already exists: {name}'))