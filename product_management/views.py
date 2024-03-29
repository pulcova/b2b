from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import OrderForm, OrderItemForm
from .models import Order, OrderItem



def order_create_view(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_item_form = OrderItemForm(request.POST)
        if order_form.is_valid() and order_item_form.is_valid():
            order = order_form.save()
            order_item = order_item_form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('employee-dashboard')
    else:
        order_form = OrderForm()
        order_item_form = OrderItemForm()
    return render(request, 'users/employee/employee_create_order.html', {'order_form': order_form, 'order_item_form': order_item_form})