# store/urls.py
from django.urls import path
from .views import home, product_list,simulate_purchase,product_detail, add_to_cart_view, cart_view,clear_cart_view

urlpatterns = [
    path('', home, name='home'),  # Ruta para la vista home
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('clear-cart/', clear_cart_view, name='clear_cart'),
    path('cart/', cart_view, name='cart'),
    path('simulate_purchase/', simulate_purchase, name='simulate_purchase'),
    
]
