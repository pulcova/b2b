from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('owner/login/', views.ownerLogin, name='owner-login'),
    path('owner/logout/', views.ownerLogout, name='owner-logout'),
    path('owner/dashboard/', views.ownerDashboard, name='owner-dashboard'),
    
    path('owner/dealer/list/', views.dealerList, name='dealer-list'),
    path('owner/dealer/orders/', views.dealerOrders, name='dealer-orders'),
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
]
