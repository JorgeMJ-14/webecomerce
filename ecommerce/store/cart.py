from django.conf import settings
from .models import Category  # Asegúrate de tener definido el modelo Category en models.py

def get_cart(request):
    """Recupera el carrito actual de la sesión."""
    cart = request.session.get('cart', {})
    return cart  

def add_to_cart(request, product_id, quantity=1):
    """Agrega un producto al carrito o actualiza la cantidad si ya existe."""
    cart = get_cart(request)  # Recupera el carrito actual
    if product_id in cart:
        cart[product_id] += quantity  # Suma la cantidad si el producto ya está en el carrito
    else:
        cart[product_id] = quantity  # Agrega el producto si no está en el carrito
    request.session['cart'] = cart  # Guarda el carrito en la sesión
    update_cart_count(request)  # Actualiza el recuento de productos en el carrito

def clear_cart(request):
    """Limpia el carrito."""
    request.session['cart'] = {}  # Resetea el carrito en la sesión
    update_cart_count(request)  # Actualiza el recuento de productos en el carrito

def update_cart_count(request):
    """Actualiza el conteo total de items en el carrito."""
    cart = get_cart(request)
    cart_count = sum(cart.values())  # Suma todas las cantidades en el carrito
    request.session['cart_count'] = cart_count  # Guarda el conteo en la sesión

def get_cart_count(request):
    """Obtiene el conteo de items en el carrito, si existe."""
    return request.session.get('cart_count', 0)

def search_cart(request, product_id):
    """Verifica si un producto específico está en el carrito."""
    cart = get_cart(request)
    return product_id in cart
