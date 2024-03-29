from django.contrib import admin

from .models import Owner, Dealer, Retailer, Employee

admin.site.register(Owner)
admin.site.register(Dealer)
admin.site.register(Retailer)
admin.site.register(Employee)
