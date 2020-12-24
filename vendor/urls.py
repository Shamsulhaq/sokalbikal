from django.urls import path

from vendor.views import (
    VendorProfileUpdateView, ItemCreateView, ItemUpdateView, VendorItemListView,
    ProductCreateView, ProductListView,
    ProductUpdateView, ProductDetailsView,OrderListView

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
    path('vendor/product/details/<slug>', ProductDetailsView.as_view(), name='vendor-product-details'),
    path('vendor/order/list/', OrderListView.as_view(), name='vendor-order-list'),

]
