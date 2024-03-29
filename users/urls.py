from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('owner/login/', views.ownerLogin, name='owner-login'),
    path('owner/logout/', views.ownerLogout, name='owner-logout'),
    path('owner/dashboard/', views.ownerDashboard, name='owner-dashboard'),

    path('owner/dealer/list/', views.dealerList, name='dealer-list'),
    path('dealer-orders/', views.dealer_orders, name='dealer-orders'),
    path('dealer/<int:dealer_id>/history/', views.dealer_purchase_history, name='dealer_purchase_history'),

    path('owner/retailer/list/', views.retailerList, name='retailer-list'),
    path('owner/retailer/orders/', views.retailerOrders, name='retailer-orders'),



    path('dealer/login/', views.dealerLogin, name='dealer-login'),
    path('dealer/logout/', views.dealerLogout, name='dealer-logout'),
    path('dealer/dashboard/', views.dealerDashboard, name='dealer-dashboard'),
    path('accept-agreement/', views.acceptAgreement, name='accept-agreement'),
    path('agreement/', views.agreement, name='agreement'),


    path('retailer/login/', views.retailerLogin, name='retailer-login'),
    path('retailer/logout/', views.retailerLogout, name='retailer-logout'),
    path('retailer/dashboard/', views.retailerDashboard, name='retailer-dashboard'),

    path('employee/login/', views.employeeLogin, name='employee-login'),
    path('employee/logout/', views.employeeLogout, name='employee-logout'),
    path('employee/dashboard/', views.employeeDashboard, name='employee-dashboard'),
    path('employee/create-dealer/', views.createDealer, name='create-dealer'),
    path('employee/create-retailer/', views.createRetailer, name='create-retailer'),
    path('employee/dealer-list/', views.userList, {'role': 'dealer'}, name='dealer-list'),
    path('employee/retailer-list/', views.userList, {'role': 'retailer'}, name='retailer-list'),
]