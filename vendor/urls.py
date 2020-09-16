from django.urls import path

from .views import (
    VendorProfileUpdateView, CreateProductView, ProductUpdateView, VendorProductListView,
    VendorProductAttributeCreateView, ProductAttributeListView,
    StockCreateView, ProductAttributeUpdateView,ProductStockListView,
    ProductStockUpdateView
)

urlpatterns = [
    path('vendor/profile/update/<slug>', VendorProfileUpdateView.as_view(), name='vendor-profile-update'),
    path('vendor/product/create', CreateProductView.as_view(), name='product-create-url'),
    path('vendor/product/update/<slug>', ProductUpdateView.as_view(), name='product-update-url'),
    path('vendor/product/list/', VendorProductListView.as_view(), name='vendor-product-list'),
    path('vendor/product/attribute/create/<slug>', VendorProductAttributeCreateView.as_view(),
         name='product-attribute-create'),
    path('vendor/product/attribute/update/<slug>', ProductAttributeUpdateView.as_view(),
         name='product-attribute-update'),
    path('vendor/product/attribute/list/', ProductAttributeListView.as_view(), name='product-attribute-list'),
    path('vendor/product/stock/manage/<slug>', StockCreateView.as_view(), name='product-stock-create'),
    path('vendor/product/stock/list/', ProductStockListView.as_view(), name='product-stock-list'),
    path('vendor/product/stock/update/<slug>', ProductStockUpdateView.as_view(), name='product-stock-update'),
]
