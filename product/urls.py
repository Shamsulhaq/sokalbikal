from django.urls import path
from .views import AllProductView,AllActiveProductList,ProductListView,ProductDetailsView

urlpatterns = [
    path('product/list/', AllProductView.as_view(), name='product-list'),
    path('product/sellable/list/', AllActiveProductList.as_view(), name='product-sellable-list'),
    path('', ProductListView.as_view(), name='product-home-url'),
    path('product/details/<slug>', ProductDetailsView.as_view(), name='product-details'),
]
