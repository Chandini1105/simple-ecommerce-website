from django.urls import path
from .views import login_page,delivery_view,payment_view,process_payment
from .views import register_page,cart,remove_item
from .views import contact_view

urlpatterns = [
    path('login/',login_page,name='login'),
    path('register',register_page,name='register'),
    path('cart/<slug>/',cart,name='cart'),
    path('remove-item/<uid>',remove_item,name='remove-item'),
    path('delivery/',delivery_view ,name='delivery'),
    path('payment/',payment_view, name='payment'),
    path('process-payment/',process_payment, name='process_payment'),
    path('contact/',contact_view, name='contact'),


]
