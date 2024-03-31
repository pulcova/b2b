from django import forms
from datetime import datetime

from .models import Order, OrderItem, Product, ProductType, Color, Size
from users.models import Dealer, Retailer

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['dealer', 'retailer']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'color', 'size', 'quantity', 'rate']