from django.shortcuts import render
from products.models import Products
from accounts.models import Cart,CartItem
# Create your views here.
def home(request):
     products=Products.objects.all()
     cart=Cart.objects.get(user=request.user) 
     entire_items=CartItem.objects.filter(cart=cart)
     count=len(entire_items)
     return render(request,'home/home.html',context={'products':products,'count':count})

