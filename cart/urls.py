from django.urls import path
from .views import cart_add,CartListView,cart_remove

urlpatterns = [
    path('product/cart/create/<pk>', cart_add, name='cart-create-url'),
    path('product/cart/list/', CartListView.as_view(), name='cart-list-url'),
    path('product/cart/remove/<pk>', cart_remove, name='cart-remove-url'),
]
