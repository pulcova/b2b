from django import forms
from datetime import datetime

from .models import Order, OrderItem, Product, ProductType, Color, Size
from users.models import Dealer, Retailer

class OrderForm(forms.ModelForm):
    dealer = forms.ModelChoiceField(queryset=Dealer.objects.all())
    retailer = forms.ModelChoiceField(queryset=Retailer.objects.all())

    class Meta:
        model = Order
        fields = ['dealer', 'retailer']

class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    product_type = forms.ModelChoiceField(queryset=ProductType.objects.all())
    design_no = forms.CharField(max_length=50)
    color = forms.ModelChoiceField(queryset=Color.objects.all())
    size_group = forms.ModelChoiceField(queryset=Size.objects.all())
    qty = forms.IntegerField(min_value=1)
    rate = forms.DecimalField(max_digits=10, decimal_places=2)
    remarks = forms.CharField(max_length=255, required=False)

    class Meta:
        model = OrderItem
        fields = ['product', 'product_type', 'design_no', 'color', 'size_group', 'qty', 'rate', 'remarks']