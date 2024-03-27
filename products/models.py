from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    images = models.ImageField(upload_to='product_images/', null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    price_for_dealer = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_sizes = models.CharField(max_length=100, null=True, blank=True)

    TAX_RATE = Decimal('0.05')

    def get_tax_amount(self):
        return self.price_for_dealer * self.TAX_RATE

    def get_price_before_tax(self):
        return self.price_for_dealer - self.get_tax_amount()

    def __str__(self):
        return self.name
    
class PurchaseBatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Purchase(models.Model):
    purchase_batch = models.ForeignKey(PurchaseBatch, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User, related_name='sales', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  
    product_name = models.CharField(max_length=255, null=True, blank=True)  
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.product:
            self.product_name = self.product.name
        super().save(*args, **kwargs)

    def __str__(self):
        product_name = self.product_name if self.product_name else 'No product'
        return f'{product_name} from {self.seller.username} to {self.buyer.username}'
    
