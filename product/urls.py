from django.urls import path
from .views import AllProductView,AllActiveProductList

urlpatterns = [
    path('product/list/', AllProductView.as_view(), name='product-list'),
    path('product/sellable/list/', AllActiveProductList.as_view(), name='product-sellable-list'),
]
