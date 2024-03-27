import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .decorators import allowed_users
from .models import Dealer, Retailer, Owner
from products.models import Purchase

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

@allowed_users(allowed_roles=['owner'])
def ownerLogout(request):
    logout(request)
    return redirect('owner-login')

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

@allowed_users(allowed_roles=['dealer'])
def dealerLogout(request):
    logout(request)
    return redirect('dealer-login')

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

@allowed_users(allowed_roles=['retailer'])
def retailerLogout(request):
    logout(request)
    return redirect('retailer-login')

@allowed_users(allowed_roles=['retailer'])
def retailerDashboard(request):
    return render(request, 'users/retailer/retailer_dashboard.html')


@allowed_users(allowed_roles=['owner'])
def dealerList(request):
    dealers = Dealer.objects.all()
    return render(request, 'users/owner/dealer_list.html', {'dealers': dealers})

@allowed_users(allowed_roles=['owner'])
def retailerList(request):
    retailers = Retailer.objects.all()
    return render(request, 'users/owner/retailer_list.html', {'retailers': retailers})


@allowed_users(allowed_roles=['owner'])
def dealerOrders(request):
    return render(request, 'users/owner/dealer_orders.html')

@allowed_users(allowed_roles=['owner'])
def retailerOrders(request):
    return render(request, 'users/owner/retailer_orders.html')