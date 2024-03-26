from django.contrib import admin

from .models import Owner, Dealer, Retailer

admin.site.register(Owner)
admin.site.register(Dealer)
admin.site.register(Retailer)
