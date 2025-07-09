from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User 
from django.contrib import messages
from store.models import Product,Profile
import datetime

def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get order
        order = Order.objects.get(id=pk)
        #get item
        items = OrderItem.objects.filter(order=pk)
        
        if request.POST:
            status = request.POST['shipping_status']
            #chech if true or false
            if status =="true":
                #get order
                order =Order.objects.filter(id=pk)
                now =datetime.datetime.now()
                order.update(shipped=True,date_shipped = now)
                messages.success(request,"update shipping order success")
                return redirect ('home')
            else:
                #get order
                order =Order.objects.filter(id=pk)
                
                now =datetime.datetime.now()
                order.update(shipped=False,date_shipped = now)
                
                messages.success(request,"update shipping order success")
                return redirect ('home')
        
        return render (request,"payment/orders.html",{"order": order,"items":items})
    else:
        messages.success(request,"access denied")
        return redirect ('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.filter(shipped=False)
        
        return render (request,"payment/not_shipped_dash.html",{"orders": order})
    else:
        messages.success(request,"access denied")
        return redirect ('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.filter(shipped=True)
        return render (request,"payment/shipped_dash.html",{"orders": order})
    else:
        messages.success(request,"access denied")
        return redirect ('home')

def process_order(request):
    if request.POST:
        cart = Cart(request)
        quantities = cart.get_quants()
        cart_products = cart.get_prods()
        totals = cart.cart_total()
        #get billing info
        payment_form = PaymentForm(request.POST or None)
        #get shippping session data
        my_shipping = request.session.get('my_shipping')
         # gather order info
        full_name = my_shipping['shipping_fullname']
        email =my_shipping['shipping_email']
        amount_paid = totals
       
        
        
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        if request.user.is_authenticated:
            #logged in
            user = request.user
            #create order
            create_order =Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            #get order id
            order_id = create_order.pk
            
            #get product info
            for product in cart_products:
                #get product id
                product_id = product.id
                 
                if product.is_sale:
                     price = product.sale_price
                else:
                    price = product.price 
                #get quantity
                for key,value in quantities.items():
                    if int(key )== product_id:
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price,)
                        create_order_item.save()
                
            #delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            # delete from database
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")
            messages.success(request,"order placed")
            return redirect ('home')
            
        else:
            create_order = Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
             #get order id
            order_id = create_order.pk
            
            #get product info
            for product in cart_products:
                #get product id
                product_id = product.id
                 
                if product.is_sale:
                     price = product.sale_price
                else:
                    price = product.price 
                #get quantity
                for key,value in quantities.items():
                    if int(key )== product_id:
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price,)
                        create_order_item.save()
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            messages.success(request,"order placed")
            return redirect ('home')
        
    else:
        messages.success(request,"Access denied")
        return redirect('home')
    
def billing_info(request):
    if request.POST:
        
        cart = Cart(request)
        quantities = cart.get_quants()
        cart_products = cart.get_prods()
        totals = cart.cart_total()
        #create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        if request.user.is_authenticated:
            billing_form=PaymentForm()
            return render (request,"payment/billing_info.html",{   'cart_products': cart_products,
                    'quantities': quantities,
                    'totals': totals,
                    'shipping_info':request.POST,
                    'billing_form':billing_form,})
        else:
            pass
        
        return render (request,"payment/billing_info.html",{   'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_form':request.POST,
                'billing_form':billing_form,})
    else:
        messages.success(request,"Access denied")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    quantities = cart.get_quants()
    cart_products = cart.get_prods()
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
       
        shipping_address, created = ShippingAddress.objects.get_or_create(user=request.user)
        shipping_form = ShippingForm(instance=shipping_address)
        
        return render(request, "payment/checkout.html", {
            
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form':shipping_form,
        })
    else:
        shipping_form = ShippingForm(request.POST,)
        return render(request, "payment/checkout.html", {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form':shipping_form,
        })
    
def payment_success(request):
    return render (request,"payment/payment_success.html",{})