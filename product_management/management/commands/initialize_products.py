import os
import random
from django.core.files import File
from django.core.management.base import BaseCommand
from product_management.models import Product, ProductType, DesignNumber, SizeGroup, Color

class Command(BaseCommand):
    help = 'Create initial products'

    def handle(self, *args, **options):
        product_names = ['Product 1', 'Product 2', 'Product 3']  # Add more product names as needed

        for product_name in product_names:
            product_type = random.choice(ProductType.objects.all())
            design_no = random.choice(DesignNumber.objects.all())
            default_size_group = random.choice(SizeGroup.objects.all())
            available_colors = random.sample(list(Color.objects.all()), 1)
            msrp = random.uniform(50, 200)  # Randomly generate MSRP between 50 and 200
            wholesale_price = msrp / 2  # Wholesale price is half of MSRP

            # Open the image file
            with open(os.path.join('media', 'product_images', 'sample_product.jpg'), 'rb') as img_file:
                product_image = File(img_file)

                product, created = Product.objects.get_or_create(
                    name=product_name,
                    defaults={
                        'type': product_type,
                        'design_no': design_no,
                        'default_size_group': default_size_group,
                        'msrp': msrp,
                        'wholesale_price': wholesale_price,
                        'images': product_image,
                    }
                )
                if created:
                    product.available_colors.set(available_colors)
                    self.stdout.write(self.style.SUCCESS(f'Product created: {product.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))

            # Close the image file
            img_file.close()