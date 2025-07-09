from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    quantities = cart.get_quants()
    cart_products = cart.get_prods()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,

    })

    
    
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        messages.success(request,("Product added to cart"))
        return JsonResponse({'qty': cart.__len__()})

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        product_name = product.name
        cart.delete(product_id)
        messages.success(request,("Product " + product_name + " deleted!!"))
        return JsonResponse({'success': True})

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product_id=product_id, quantity=product_qty)
        messages.success(request,("Product quantity updated!!"))
        return JsonResponse({'success': True, 'qty': product_qty})