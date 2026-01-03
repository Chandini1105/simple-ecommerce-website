from django.db import models
from django.contrib.auth.models import User 
from base.models import BaseModel
# Create your models here.
from products.models import Products,ColorVariant,SizeVariant


class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=4)
    image=models.ImageField(upload_to='profile')
    
class Cart(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    

class CartItem(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    size=models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
    color=models.ForeignKey(ColorVariant,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=1)
    
    def total_cost(self):
        return self.product.price*self.quantity
    

    