from django.shortcuts import get_object_or_404, render, redirect
from . models import Product, Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,changePasswordForm,UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
import json

from cart.cart import Cart

def search(request):
    category = Category.objects.all()
    #determine if the filled up the form
    if request.method == 'POST':
        searched = request.POST['searched']
        
        # Query the products db models
        searched = Product.objects.filter (Q(name__icontains = searched) | Q(description__icontains= searched))
        
        if not searched:
             messages.success(request,"this Product not exist")
             return render(request,"search.html",{'searched':searched})
        else :
            return render(request,"search.html",{'searched':searched}) 
        
    else:
        return render(request,"search.html",{'categorys': category}) 


def update_info(request):
    if request.user.is_authenticated:
        try:
            # Get the profile and shipping address for the current user
            current_user_profile = Profile.objects.get(user=request.user)
            shipping_address, created = ShippingAddress.objects.get_or_create(user=request.user)

            if request.method == 'POST':
                form = UserInfoForm(request.POST, instance=current_user_profile)
                shipping_form = ShippingForm(request.POST, instance=shipping_address)

                if form.is_valid() or shipping_form.is_valid():
                    form.save()
                    shipping_form.save()
                    messages.success(request, "Your information has been updated!")
                    return redirect('home')
            else:
                # For GET requests, populate forms with existing data
                form = UserInfoForm(instance=current_user_profile)
                shipping_form = ShippingForm(instance=shipping_address)

            return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})

        except Profile.DoesNotExist:
            messages.error(request, "User profile not found.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to access this page!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = changePasswordForm(current_user,request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request,"update success!!")
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password')
        else:
            form = changePasswordForm(current_user)
            return render(request,"update_password.html",{'form':form})
    else:
        messages.success(request,"You MUST be logged in to  access this page!!!!")
        return redirect('home')
    
   

def update_user(request):
    if request.user.is_authenticated:
        current_users =User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_users)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request,current_users)
            messages.success(request,"User has Been Updated!!")
            return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form})    
    else:
         messages.success(request,"You MUST be logged in to  access this page!!!!")
         return redirect('home')
    
def category_summary(request):
    return render(request,'category_summary.html',{})

def category( request ,catname ):    
    category = Category.objects.get(name = catname)
    products = Product.objects.filter(category=category)
    
    return render(request,'category.html',{'category': category,
        'products': products})

def product( request , pk ):   
    categorys = Category.objects.all() 
    products = Product.objects.get(id  = pk)
    return render(request,'product.html',{'product': products,'categorys': categorys })

def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
    return render(request,'home.html',{'products': products,'categorys': category })

def about(request):
    category = Category.objects.all()
    return render(request,'about.html',{'categorys': category})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            current_user =Profile.objects.get(user__id = request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity = value)
                
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')
    
    return render(request, 'login.html', {})



def logout_user(request):

    logout(request)
    messages.success(request,"thank you")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You Have Registered!!welcome!!"))
            return redirect('home')
        else:
            print("Form errors:", form.errors.as_json())
            messages.success(request,("Whoops!..there is a problem..please try again"))
            return redirect('register')
    else:
        print("Form errors:", form.errors) 
        return render(request, 'register.html', {'form':form})
    