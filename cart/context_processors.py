from .cart import Cart

def cart(request):
    return {
        'cart': Cart(request),
        'cart_items_count': len(Cart(request))  # Explicit count
    }