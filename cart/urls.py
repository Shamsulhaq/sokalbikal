from django.urls import path
from .views import cart_add

urlpatterns = [
    path('product/cart/create/<pk>', cart_add, name='cart-create-url'),
]
