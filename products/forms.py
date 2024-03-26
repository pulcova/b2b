from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'available_sizes', 'category', 'images', 'stock_quantity', 'price_for_dealer', 'maximum_retail_price']

class PurchaseForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Select Product")
    size = forms.CharField(max_length=100)
    quantity = forms.IntegerField(min_value=1)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)


    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')

        if product and quantity:
            if quantity > product.stock_quantity:
                self.add_error('quantity', 'Not enough stock for this product')