from django.core.management.base import BaseCommand
from product_management.models import ProductType 
class Command(BaseCommand):
    help = 'Create initial product types'

    def handle(self, *args, **options):
        product_types = [
            ('Jeans Pant', 'Jeans Pant'),
            ('T-shirt', 'T-shirt'),
            ('Formal Shirt', 'Formal Shirt'),
            ('Casual Shirt', 'Casual Shirt'),
            # Add more product types as needed
        ]

        for name, display_name in product_types:
            product_type, created = ProductType.objects.get_or_create(
                name=name, 
                defaults={'name': display_name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Product type created: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product type already exists: {name}'))