import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Size  

class Command(BaseCommand):
    help = 'Injects sizes from a file into the database'

    def handle(self, *args, **kwargs):
        static_dir = settings.STATICFILES_DIRS[0]
        file_path = os.path.join(static_dir, 'sizes', 'sizes.txt')  
        with open(file_path, 'r') as f:
            for size_name in f:
                size_name = size_name.strip()  
                size, created = Size.objects.get_or_create(name=size_name)
                if created:
                    self.stdout.write(f"Size {size_name} created successfully")
                else:
                    self.stdout.write(f"Size {size_name} already exists")
