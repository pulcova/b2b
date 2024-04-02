from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import OrderForm, OrderItemForm
from .models import Order, OrderItem, Product, Color, Size

from users.models import Dealer, Retailer
from django.forms import inlineformset_factory
from django.db import transaction

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
)

@login_required
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.sales_employee = request.user.employee
            order.save()
            return redirect('add-order-items', order_id=order.pk)
    else:
        order_form = OrderForm()
        dealers = Dealer.objects.all()
        retailers = Retailer.objects.all()
    return render(request, 'users/employee/employee_create_order.html', {'order_form': order_form, 'dealers': dealers, 'retailers': retailers})

@login_required
def add_order_items(request, order_id):
    order = Order.objects.get(pk=order_id)
    products = Product.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    if request.method == 'POST':
        order_item_formset = OrderItemFormSet(request.POST, instance=order)
        if order_item_formset.is_valid():
            for form in order_item_formset:
                product = form.cleaned_data['product']
                color = form.cleaned_data['color']
                size = form.cleaned_data['size']
                quantity = form.cleaned_data['quantity']
                rate = form.cleaned_data['rate']

                order_item = {
                    'product': product.id,
                    'color': color.id,
                    'size': size.id,
                    'quantity': quantity,
                    'rate': str(rate)
                }
                request.session['cart'] = request.session.get('cart', [])
                request.session['cart'].append(order_item)

            return redirect('add-order-items', order_id=order.pk)
    else:
        order_item_formset = OrderItemFormSet(instance=order)
        cart = request.session.get('cart', [])
        for item in cart:
            item['product'] = get_object_or_404(Product, id=item['product'])
            item['color'] = get_object_or_404(Color, id=item['color'])
            item['size'] = get_object_or_404(Size, id=item['size'])
    return render(request, 'users/employee/employee_add_order_items.html', {'order_item_formset': order_item_formset, 'order': order, 'cart': cart, 'products': products, 'colors': colors, 'sizes': sizes})

@login_required
def finalize_order(request, order_id):
    with transaction.atomic():
        order = Order.objects.get(pk=order_id)
        order.status = 'PA'
        order.save()

        for item in request.session['cart']:

            product = Product.objects.get(id=item['product'])
            color = Color.objects.get(id=item['color'])
            size = Size.objects.get(id=item['size'])
            quantity = item['quantity']
            rate = Decimal(item['rate'])

            order_item = OrderItem(
                order=order,
                product=product,
                color=color,
                size=size,
                quantity=quantity,
                rate=rate
            )
            order_item.save()
        request.session['cart'] = []
    return redirect('view-orders')

@login_required
def view_orders(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
    elif request.user.employee:
        orders = Order.objects.filter(sales_employee=request.user.employee)
    else:
        orders = Order.objects.filter(dealer=request.user.dealer)

    context = {
        'orders': orders
    }
    return render(request, 'users/employee/employee_view_orders.html', context)

@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'users/employee/employee_order_summary.html', {'order': order})

