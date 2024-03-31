from django.db import models

from users.models import Dealer, Retailer, Employee

class ProductType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name 

class SizeGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    sizes = models.ManyToManyField('Size')

    def __str__(self):
        sizes = ", ".join([str(size) for size in self.sizes.all()])
        return f"{self.name} ({sizes})"

class Size(models.Model):
    name = models.CharField(max_length=10)  

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True) 

    def __str__(self):
        return self.name
    
class DesignNumber(models.Model):
    design_no = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.design_no

class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    design_no = models.ForeignKey(DesignNumber, on_delete=models.PROTECT)
    images = models.ImageField(upload_to='media/product_images/')

    default_size_group = models.ForeignKey(SizeGroup, on_delete=models.SET_NULL, null=True, blank=True)
    available_colors = models.ManyToManyField(Color)

    msrp = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('PI', 'Pending Invoice'),
        ('PP', 'Pending Payment'),
        ('PD', 'Paid'),
    ]

    order_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.PROTECT)
    retailer = models.ForeignKey(Retailer, on_delete=models.PROTECT)
    sales_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PP')

    def __str__(self):
        return f"Order {self.order_id}"
    
class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order Item {self.order_item_id}"
    
class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('PD', 'Paid'),
        ('O', 'Overdue'),
    ]

    invoice_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    invoice_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField()
    customer_id = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15)
    waybill_number = models.CharField(max_length=255)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2)
    courier_name = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, default='P')

    def __str__(self):
        return f"Invoice {self.invoice_id}"