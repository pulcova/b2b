from django.contrib import admin

from .models import Product, ProductType, Size, SizeGroup, Color, Order, OrderItem, Invoice, DesignNumber

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Size)
admin.site.register(SizeGroup)
admin.site.register(Color)
admin.site.register(DesignNumber)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Invoice)