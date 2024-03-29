from django.urls import path

from . import views
from product_management import views as product_views

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
    path('dealer/create-retailer/', views.DealerCreateRetailer, name='dealer-create-retailer'),
    path('dealer/retailer-list/', views.DealerRetailerList, name='dealer-retailer-list'),



    path('employee/login/', views.employeeLogin, name='employee-login'),
    path('employee/logout/', views.employeeLogout, name='employee-logout'),
    path('employee/dashboard/', views.employeeDashboard, name='employee-dashboard'),
    path('employee/create-dealer/', views.createDealer, name='employee-create-dealer'),
    path('employee/create-retailer/', views.EmployeeCreateRetailer, name='employee-create-retailer'),
    path('employee/dealer-list/', views.userList, {'role': 'dealer'}, name='employee-dealer-list'),
    path('employee/retailer-list/', views.userList, {'role': 'retailer'}, name='employee-retailer-list'),
    path('employee/create-order/', product_views.order_create_view, name='create-order'),
]