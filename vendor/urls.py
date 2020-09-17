from django.urls import path

from .views import (
    VendorProfileUpdateView, ItemCreateView, ItemUpdateView, VendorItemListView,
    ProductCreateView, ProductListView,
    ProductUpdateView

)

urlpatterns = [
    path('vendor/profile/update/<pk>', VendorProfileUpdateView.as_view(), name='vendor-profile-update'),
    path('vendor/item/create', ItemCreateView.as_view(), name='item-create-url'),
    path('vendor/item/update/<slug>', ItemUpdateView.as_view(), name='item-update-url'),
    path('vendor/item/list/', VendorItemListView.as_view(), name='vendor-item-list'),
    path('vendor/product/create/<slug>', ProductCreateView.as_view(),
         name='product-create'),
    path('vendor/product/update/<slug>', ProductUpdateView.as_view(),
         name='product-update'),
    path('vendor/product/list/', ProductListView.as_view(), name='vendor-product-list'),
    # path('vendor/product/stock/manage/<slug>', StockCreateView.as_view(), name='product-stock-create'),
    # path('vendor/product/stock/list/', ProductStockListView.as_view(), name='product-stock-list'),
    # path('vendor/product/stock/update/<slug>', ProductStockUpdateView.as_view(), name='product-stock-update'),
]
