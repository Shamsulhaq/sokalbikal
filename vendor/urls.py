from django.urls import path

from .views import (
    VendorProfileUpdateView,VendorProductListView,VendorProductAttributeCreateView,ProductAttributeListView
)

urlpatterns = [
    path('vendor/profile/update/<slug>', VendorProfileUpdateView.as_view(), name='vendor-profile-update'),
    path('vendor/product/list/', VendorProductListView.as_view(), name='vendor-product-list'),
    path('vendor/product/attribute/create/<slug>', VendorProductAttributeCreateView.as_view(), name='product-attribute-create'),
    path('vendor/product/attribute/list/', ProductAttributeListView.as_view(), name='product-attribute-list'),
]
