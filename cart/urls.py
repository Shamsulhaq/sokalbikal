from django.urls import path
from .views import cart_add,CartListView

urlpatterns = [
    path('product/cart/create/<pk>', cart_add, name='cart-create-url'),
    path('product/cart/list/', CartListView.as_view(), name='cart-list-url'),
]
