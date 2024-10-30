from .models import Category

def categories_processor(request):
    # Obtiene todas las categorías
    categories = Category.objects.all()
    
    # Obtiene el número de productos en el carrito
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())  # Suma la cantidad total de productos en el carrito

    # Devuelve las variables para el contexto global
    return {
        'categories': categories,
        'cart_count': cart_count,
    }
