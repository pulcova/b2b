import os
from django.core.management.base import BaseCommand
from django.conf import settings  
from products.models import Color  

class Command(BaseCommand):
    help = 'Injects colors from a file into the database'

    def handle(self, *args, **kwargs):
        static_dir = settings.STATICFILES_DIRS[0]
        file_path = os.path.join(static_dir, 'colors', 'colors.txt') 
        with open(file_path, 'r') as f:
            for color_name in f:
                color_name = color_name.strip()
                color, created = Color.objects.get_or_create(name=color_name)
                if created:
                    self.stdout.write(f"Color {color_name} created successfully")
                else:
                    self.stdout.write(f"Color {color_name} already exists")
