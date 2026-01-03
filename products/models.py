from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.

class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to='categories')
    slug=models.SlugField(unique=True,null=True,blank=True)
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.category_name
class ColorVariant(BaseModel):
    color=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.color
       
class SizeVariant(BaseModel):
    size=models.CharField(max_length=10,null=True,blank=True)
    def __str__(self):
        return self.size
    
        
class Products(BaseModel):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    product_name=models.CharField(max_length=100)
    price=models.FloatField()
    description=models.TextField() 
    slug=models.SlugField(unique=True,null=True,blank=True)
    size=models.ManyToManyField(SizeVariant,related_name='sizes',null=True,blank=True)
    color=models.ManyToManyField(ColorVariant,related_name='colors',null=True,blank=True)
    def save(self,*args,**kwargs):
        self.slug=slugify(self.product_name)
        super(Products,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.product_name
    
class ProductImage(BaseModel):
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_image')
    image=models.ImageField(upload_to='products')
        

       
       