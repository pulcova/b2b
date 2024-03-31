from django.core.management.base import BaseCommand
from product_management.models import DesignNumber  # Replace 'product_management' with your Django app's name

class Command(BaseCommand):
    help = 'Create initial design numbers'

    def handle(self, *args, **options):
        design_numbers = [
            'DN001',
            'DN002',
            'DN003',
            # Add more design numbers as needed
        ]

        for design_no in design_numbers:
            design_number, created = DesignNumber.objects.get_or_create(
                design_no=design_no
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Design number created: {design_no}'))
            else:
                self.stdout.write(self.style.WARNING(f'Design number already exists: {design_no}'))