from django.contrib import admin

from .models import Product, Purchase, PurchaseBatch

admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseBatch)
