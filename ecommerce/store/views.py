from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .cart import add_to_cart, clear_cart, get_cart
from django import forms
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.shortcuts import redirect

# Vista de inicio que muestra los primeros 6 productos
def home(request):
    products = Product.objects.all()[:6]
    return render(request, 'store/home.html', {'products': products})

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
