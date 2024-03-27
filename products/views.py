import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from decimal import Decimal
from django.http import HttpResponse, FileResponse
from django.db import transaction
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO


from .forms import ProductForm, PurchaseForm
from .models import Product, Purchase, PurchaseBatch
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
    # Start a transaction
    with transaction.atomic():
        # Create a PurchaseBatch
        purchase_batch = PurchaseBatch.objects.create(user=request.user)

        # Get the cart from the session
        cart = request.session.get('cart', [])

        # Loop over the items in the cart
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
                purchase_batch=purchase_batch,
                seller=admin_user,
                buyer=request.user,
                product=product,
                size=purchase['size'],
                quantity=purchase['quantity'],
                total_price=Decimal(purchase['total_price'])  # Convert back to Decimal
            )

        # Clear the cart
        request.session['cart'] = []

    # Redirect to the checkout success page
    return redirect('checkout-success')

def clear_cart(request):
    request.session['cart'] = []
    return HttpResponse(status=204)

def checkout_success(request):
    return render(request, 'users/dealer/checkout_success.html')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@allowed_users(allowed_roles=['dealer'])
def purchase_history(request):
    purchase_batches = PurchaseBatch.objects.filter(user=request.user)

    if request.method == 'POST' and 'generate_invoice' in request.POST:
        batch_id = request.POST.get('batch_id')
        batch = get_object_or_404(PurchaseBatch, pk=batch_id)
        purchases = batch.purchase_set.all()

        purchases_with_tax = [
            {
                'purchase': purchase,
                'tax_amount_per_unit': purchase.product.get_tax_amount(),
                'tax_amount': purchase.product.get_tax_amount() * purchase.quantity,
                'price_befor_tax_per_unit': purchase.product.get_price_before_tax(),
                'price_before_tax': purchase.product.get_price_before_tax() * purchase.quantity,
            }
            for purchase in purchases
        ]

        total_price = sum(purchase.total_price for purchase in purchases)
        pdf = render_to_pdf('users/invoice.html', {'batch': batch, 'purchases_with_tax': purchases_with_tax, 'total_price': total_price})
        return HttpResponse(pdf, content_type='application/pdf')

    return render(request, 'users/dealer/purchase_history.html', {'purchase_batches': purchase_batches})
