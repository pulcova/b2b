from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from decimal import Decimal
from django.http import HttpResponse


from .forms import ProductForm, PurchaseForm
from .models import Product, Purchase
from users.decorators import allowed_users

@allowed_users(allowed_roles=['owner'])
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.errors)
            form.save()
            return redirect('create-product')
    else:
        form = ProductForm()
    return render(request, 'users/owner/create_product.html', {'form': form})

@allowed_users(allowed_roles=['owner'])
def product_list(request):
    products = Product.objects.all()
    return render(request, 'users/owner/product_list.html', {'products': products})

@allowed_users(allowed_roles=['dealer'])
def puchase_products(request):
    return render(request, 'users/dealer/purchase_products.html')

@allowed_users(allowed_roles=['dealer'])
def new_purchase(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            size = form.cleaned_data['size']
            quantity = form.cleaned_data['quantity']

            # Add the purchase to the session data
            purchase = {
                'product': product.id,
                'product_name': product.name,
                'size': size,
                'quantity': quantity,
                'total_price': str(product.price_for_dealer * quantity)  # Convert to str
            }
            request.session['cart'] = request.session.get('cart', [])
            request.session['cart'].append(purchase)

            # Redirect to the same page to display a new form
            return redirect('new-purchase')
    else:
        # Clear the session data when displaying a new form
        form = PurchaseForm()
    return render(request, 'users/dealer/new_purchase.html', {'form': form, 'products': products})

@allowed_users(allowed_roles=['dealer'])
def checkout(request):
    cart = request.session.get('cart', [])
    for purchase in cart:
        # Get the product
        product = Product.objects.get(id=purchase['product'])

        # Update the stock quantity
        product.stock_quantity -= purchase['quantity']
        product.save()

        # Get the admin user
        admin_group = Group.objects.get(name='owner')
        admin_user = admin_group.user_set.first()

        # Create a new Purchase object
        Purchase.objects.create(
            seller=admin_user,
            buyer=request.user,
            product=product,
            size=purchase['size'],
            quantity=purchase['quantity'],
            total_price=Decimal(purchase['total_price'])  # Convert back to Decimal
        )

    # Clear the cart
    request.session['cart'] = []
    return redirect('checkout-success')

def clear_cart(request):
    request.session['cart'] = []
    return HttpResponse(status=204)

def checkout_success(request):
    return render(request, 'users/dealer/checkout_success.html')