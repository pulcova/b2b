import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, FileResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


from .forms import DealerForm, RetailerForm
from .decorators import allowed_users
from .models import Dealer, Retailer, Owner
from products.models import Purchase, PurchaseBatch, Product
from products.utils import render_to_pdf

# Home view

def home(request):
    return render(request, 'users/base/base.html')

def session_expired(request):
    return render(request, 'users/base/session_expired.html')

# Login, logout, dashboard views

def genericLogin(request, role, redirect_page):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if role == 'dealer':
                return handle_dealer_login(request, user, redirect_page)
            else:
                return redirect(redirect_page)

    return render(request, f'users/{role}/{role}_login.html')

def handle_dealer_login(request, user, redirect_page):
    dealer = Dealer.objects.get(user=user)
    if not dealer.agreement_accepted:
        return HttpResponseRedirect(reverse('agreement'))
    return redirect(redirect_page)


# owner views - login, logout, dashboard, dealer_list, retailer_list, dealer_orders, dealer_purchase_history, retailer_orders

def ownerLogin(request):
    return genericLogin(request, 'owner', 'owner-dashboard')

@login_required
@allowed_users(allowed_roles=['owner'])
def ownerLogout(request):
    logout(request)
    return redirect('home')

@login_required
@allowed_users(allowed_roles=['owner'])
def ownerDashboard(request):
    return render(request, 'users/owner/owner_dashboard.html')

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

# dealer views - login, logout, dashboard, agreement

def dealerLogin(request):
    return genericLogin(request, 'dealer', 'dealer-dashboard')

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

# dealer views - create retailer, view retailers

@login_required
@allowed_users(allowed_roles=['dealer'])
def DealerCreateRetailer(request):
    if request.method == 'POST':
        form = RetailerForm(request.POST)
        if form.is_valid():
            retailer = form.save(commit=False)
            retailer.created_by = request.user
            retailer.save()
            return redirect('dealer-retailer-list')  
    else:
        form = RetailerForm()
    return render(request, 'users/dealer/dealer_create_retailer.html', {'form': form})

@login_required
@allowed_users(allowed_roles=['dealer'])
def DealerRetailerList(request):
    retailers = Retailer.objects.filter(created_by=request.user)
    return render(request, 'users/dealer/dealer_retailer_list.html', {'retailers': retailers})

# retailer views - login, logout, dashboard


@login_required
@allowed_users(allowed_roles=['retailer'])
def retailerDashboard(request):
    return render(request, 'users/retailer/retailer_dashboard.html')


# EMPLOYEE VIEWS
# employee/sales person views - login, logout, dashboard

def employeeLogin(request):
    return genericLogin(request, 'employee', 'employee-dashboard')

@login_required
@allowed_users(allowed_roles=['employee'])
def employeeLogout(request):
    logout(request)
    return redirect('home')

@login_required
@allowed_users(allowed_roles=['employee'])
def employeeDashboard(request):
    return render(request, 'users/employee/employee_dashboard.html')

# employee views - create dealer, create retailer

@login_required
@allowed_users(allowed_roles=['employee'])
def createDealer(request):
    if request.method == 'POST':
        form = DealerForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            group = Group.objects.get(name='dealer')
            user.groups.add(group)
            dealer = Dealer(user=user, 
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            phone=form.cleaned_data['phone'],
                            email=form.cleaned_data['email'],
                            profile_pic=form.cleaned_data['profile_pic'])
            dealer.save()
            return redirect('employee-dashboard')
    else:
        form = DealerForm()
    return render(request, 'users/employee/employee_create_dealer.html', {'form': form})

@login_required
@allowed_users(allowed_roles=['employee'])
def EmployeeCreateRetailer(request):
    if request.method == 'POST':
        form = RetailerForm(request.POST)
        if form.is_valid():
            retailer = form.save(commit=False)
            retailer.created_by = request.user
            retailer.save()
            return redirect('employee-retailer-list')  
    else:
        form = RetailerForm()
    return render(request, 'users/employee/employee_create_retailer.html', {'form': form})

# employee views - view dealers, view retailers

@login_required
def userList(request, role):
    if role == 'dealer':
        users = Dealer.objects.filter(created_by=request.user)
        template_name = 'users/employee/employee_dealer_list.html'
    elif role == 'retailer':
        users = Retailer.objects.filter(created_by=request.user)
        template_name = 'users/employee/employee_retailer_list.html'
    else:
        return HttpResponseBadRequest("Invalid role")

    return render(request, template_name, {'users': users})