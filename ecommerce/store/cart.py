from django.conf import settings

def get_cart(request):
    cart = request.session.get('cart', {})
    return cart  # Debe devolver un diccionario con {product_id: quantity}

def add_to_cart(request, product_id, quantity):
    """Agrega un producto al carrito, sumando la cantidad si ya existe."""
    cart = get_cart(request)  # Recupera el carrito actual
    if product_id in cart:
        cart[product_id] += quantity  # Suma la cantidad si el producto ya está en el carrito
    else:
        cart[product_id] = quantity  # Agrega el producto si no está en el carrito
    request.session['cart'] = cart  # Guarda el carrito en la sesión

def clear_cart(request):
    """Limpia el carrito."""
    request.session['cart'] = {}  # O la forma en que estés almacenando el carrito
