from django.urls import path

from . import views

urlpatterns = [
    path('create-product/', views.create_product, name='create-product'),
    path('product-list/', views.product_list, name='product-list'),
    path('purchase-products/', views.puchase_products, name='purchase-products'),
    path('new-purchase/', views.new_purchase, name='new-purchase'),
    path('checkout/', views.checkout, name='checkout'),
    path('clear-cart/', views.clear_cart, name='clear-cart'),
    path('checkout-success/', views.checkout_success, name='checkout-success'),
    path('purchase-history/', views.purchase_history, name='purchase-history'),
]