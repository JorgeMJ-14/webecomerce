# store/urls.py
from django.urls import path
from .views import (
    home, 
    product_list,
    simulate_purchase,
    product_detail, 
    add_to_cart_view, 
    cart_view,
    clear_cart_view,
    search,           # Asegúrate de incluir estas funciones en la importación
    get_cart_count ,
    remove_from_cart   # Asegúrate de incluir estas funciones en la importación
)

urlpatterns = [
    path('', home, name='home'),  # Ruta para la vista home
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('clear-cart/', clear_cart_view, name='clear_cart'),
    path('cart/', cart_view, name='cart'),
    path('simulate_purchase/', simulate_purchase, name='simulate_purchase'),
    path('search/', search, name='search'),          # Usa 'search' directamente
    path('get_cart_count/', get_cart_count, name='get_cart_count'), 
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
]
