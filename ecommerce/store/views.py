from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,Category
from .cart import add_to_cart, clear_cart, get_cart
from django import forms
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.shortcuts import redirect

# Vista de inicio que muestra los primeros 6 productos
def home(request):
    categories = Category.objects.all()  # Incluye las categorías en el contexto
    return render(request, 'store/home.html', {'categories': categories})

# Formulario para agregar productos al carrito
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

# Vista para mostrar los detalles del producto
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            add_to_cart(request, product_id, quantity)  # Agrega el producto al carrito
            return redirect('cart')  # Redirige al carrito después de agregar
    else:
        form = AddToCartForm()  # Crea una nueva instancia del formulario

    return render(request, 'store/product_detail.html', {'product': product, 'form': form})

# Vista para listar todos los productos
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# Vista para agregar un producto al carrito
def add_to_cart_view(request, product_id):
    quantity = int(request.POST.get('quantity', 1))  # Obtiene la cantidad desde el formulario
    add_to_cart(request, product_id, quantity)  # Agrega el producto al carrito
    return redirect('cart')  # Redirige al carrito

# Vista para mostrar el carrito
def cart_view(request):
    cart = get_cart(request)  # Obtiene el carrito de la sesión
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)  # Obtiene el producto
        total += product.price * quantity  # Calcula el total
        products.append({'product': product, 'quantity': quantity})

    context = {
        'products': products,
        'total': total,
    }
    return render(request, 'store/cart.html', context)

# Vista para simular la compra y generar un recibo en PDF
def simulate_purchase(request):
    cart = get_cart(request)  # Obtiene el carrito
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)  # Obtiene el producto
        total += product.price * quantity  # Calcula el total
        products.append({'product': product, 'quantity': quantity})

    # Generar PDF
    context = {
        'products': products,
        'total': total,
    }
    html = render_to_string('store/receipt.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def clear_cart_view(request):
    """Vista para limpiar el carrito."""
    clear_cart(request)  # Llama a la función para limpiar el carrito
    return redirect('cart')  # Redirige al carrito

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)  # Filtra por nombre del producto

    return render(request, 'store/search_results.html', {'results': results, 'query': query})

def get_cart_count(request):
    cart_count = request.session.get('cart_count', 0)  # Supongamos que mantienes el conteo en la sesión
    return JsonResponse({'cart_count': cart_count})

# store/views.py
from django.shortcuts import redirect

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart  # Actualizar el carrito en la sesión
    return redirect('cart')  # Redirigir de nuevo a la página del carrito

