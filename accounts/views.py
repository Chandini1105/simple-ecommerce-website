from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
import random
from .models import Cart,CartItem
from products.models import Products,SizeVariant,ColorVariant
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        obj=User.objects.filter(username=username)
        if not obj.exists():
            messages.warning(request,'Email is not registered')
            return redirect('login')
        user=authenticate(request,username=username,password=password)
        if user==None:
            messages.warning(request,'Invalid password')
            return redirect('login')
        login(request,user)
        return redirect('home')
    
    return render(request,'accounts/login.html')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        data=request.POST
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        username=data.get('username')
        password=data.get('password')
        confirm_password=data.get('confirm_password')
        obj=User.objects.filter(username=username)
        if obj.exists():
            messages.warning(request,'Email already exists')
            return redirect('register')
        if password!=confirm_password:
             messages.warning(request,'Password doesnt match')
             return redirect('register')
        # otp=random.randint(1000,9999)
        # send_mail(username,otp)    
        new_user=User.objects.create(first_name=first_name,last_name=last_name,username=username)
        # new_user.profile.email_token=otp
        new_user.set_password(password)
        new_user.save()    
        messages.warning(request,'Successfully registered')
    
    return render(request,'accounts/register.html')

def cart(request,slug):
    cart=Cart.objects.get(user=request.user)
    entire_items=CartItem.objects.filter(cart=cart)
    count=len(entire_items)
    if request.method=='POST':
        data=request.POST
        color=data.get('color')
        size=data.get('size')
        quantity=data.get('quantity')
        
        if not Cart.objects.filter(user=request.user).exists():
            cart=Cart.objects.create(user=request.user)
        else:
            cart=Cart.objects.get(user=request.user)
        product=Products.objects.get(slug=slug)
        if SizeVariant.objects.filter(size=size).exists():
            size=SizeVariant.objects.get(size=size)
        else:
            size=None
        if ColorVariant.objects.filter(color=color).exists():
            color=ColorVariant.objects.get(color=color)
        else:
            color=None
        created=CartItem.objects.filter(cart=cart,product=product)
        
        if created:   
            created[0].quantity+=int(quantity)
            created[0].save()    
        else:           
            CartItem.objects.create(
                cart=cart,
                product=product,
                size=size,
                color=color,
                quantity=quantity,
        )
        return redirect('cart',None)
    cart=Cart.objects.get(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart) 
    totalcost=0
    for item in cart_items:
        totalcost+=item.total_cost()
    return render(request,'cart/cart.html',{'cart_items':cart_items,'totalcost':totalcost,'count':count})

def remove_item(request,uid):
    cart=Cart.objects.get(user=request.user)
    cart_item=CartItem.objects.get(cart=cart,uid=uid)
    if cart_item:
        cart_item.delete()
        return redirect('cart',None)
    else:
        print('Item not present in cart') 

def delivery_view(request):
    cart=Cart.objects.get(user=request.user)
    entire_items=CartItem.objects.filter(cart=cart)
    count=len(entire_items)
    return render(request, 'delivery/delivery.html',{'count':count})

def payment_view(request):
    cart=Cart.objects.get(user=request.user)
    entire_items=CartItem.objects.filter(cart=cart)
    count=len(entire_items)
    return render(request, 'payment/payment.html',{'count':count})

def process_payment(request):
    cart=Cart.objects.get(user=request.user)
    entire_items=CartItem.objects.filter(cart=cart)
    count=len(entire_items)
    if request.method == 'POST':
        cardholder = request.POST['cardholder']
        cardnumber = request.POST['cardnumber']
        expiry = request.POST['expiry']
        cvv = request.POST['cvv']
        
        return redirect('success_page',None)  
    return render(request, 'payment/payment.html',{'count':count})

def contact_view(request):
    cart=Cart.objects.get(user=request.user)
    entire_items=CartItem.objects.filter(cart=cart)
    count=len(entire_items)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        full_message = f"Message from {name} ({email}):\n\n{message}"
        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            ['your-email@example.com'],  
        )
        return redirect('success_page',None) 
    return render(request, 'contact/contact.html',{'count':count})

        
        

        
    








