from django.urls import path
from .views import AllProductView, AllActiveProductList, PubProductListView, PubProductDetailsView


urlpatterns = [
    path('admin/product/list/', AllProductView.as_view(), name='product-list-url'),
    path('admin/product/sellable/list/', AllActiveProductList.as_view(), name='product-sellable-list-url'),
    path('', PubProductListView.as_view(), name='product-home-url'),
    path('product/details/<slug>', PubProductDetailsView.as_view(), name='customer-product-details-url'),
]
