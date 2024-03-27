import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users
from .models import Dealer, Retailer, Owner
from products.models import Purchase, PurchaseBatch, Product
from products.utils import render_to_pdf

def home(request):
    return render(request, 'users/base/base.html')

def ownerLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('owner-dashboard')

    return render(request, 'users/owner/owner_login.html')

@login_required
@allowed_users(allowed_roles=['owner'])
def ownerLogout(request):
    logout(request)
    return redirect('home')

@login_required
@allowed_users(allowed_roles=['owner'])
def ownerDashboard(request):
    return render(request, 'users/owner/owner_dashboard.html')

def dealerLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            dealer = Dealer.objects.get(user=user)
            if not dealer.agreement_accepted:
                return HttpResponseRedirect(reverse('agreement'))
            return redirect('dealer-dashboard')

    return render(request, 'users/dealer/dealer_login.html')

def acceptAgreement(request):
    if request.method == 'POST':
        user = request.user
        dealer = Dealer.objects.get(user=user)
        dealer.agreement_accepted = True
        dealer.save()
        return redirect('dealer-dashboard')

    return render(request, 'users/dealer/agreement.html')
    
def agreement(request):
    return render(request, 'users/dealer/agreement.html')

@login_required
@allowed_users(allowed_roles=['dealer'])
def dealerLogout(request):
    logout(request)
    return redirect('home')

@login_required
@allowed_users(allowed_roles=['dealer'])
def dealerDashboard(request):
    return render(request, 'users/dealer/dealer_dashboard.html')

def retailerLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('retailer-dashboard')

    return render(request, 'users/retailer/retailer_login.html')

@login_required
@allowed_users(allowed_roles=['retailer'])
def retailerLogout(request):
    logout(request)
    return redirect('home')

@login_required
@allowed_users(allowed_roles=['retailer'])
def retailerDashboard(request):
    return render(request, 'users/retailer/retailer_dashboard.html')


@login_required
@allowed_users(allowed_roles=['owner'])
def dealerList(request):
    dealers = Dealer.objects.all()
    return render(request, 'users/owner/dealer_list.html', {'dealers': dealers})

@login_required
@allowed_users(allowed_roles=['owner'])
def retailerList(request):
    retailers = Retailer.objects.all()
    return render(request, 'users/owner/retailer_list.html', {'retailers': retailers})


@login_required
@allowed_users(allowed_roles=['owner'])
def dealer_orders(request):
    dealers = Dealer.objects.all()
    context = {'dealers': dealers}
    return render(request, 'users/owner/dealer_orders.html', context)

@login_required
@allowed_users(allowed_roles=['owner'])
def dealer_purchase_history(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id) 
    purchases = Purchase.objects.filter(buyer=dealer.user, seller=request.user) 
    purchase_batches = PurchaseBatch.objects.filter(user=dealer.user)

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
    
    context = {'dealer': dealer, 'purchases': purchases, 'purchase_batches': purchase_batches}
    return render(request, 'users/owner/dealer_order_history.html', context)

@login_required
@allowed_users(allowed_roles=['owner'])
def retailerOrders(request):
    return render(request, 'users/owner/retailer_orders.html')