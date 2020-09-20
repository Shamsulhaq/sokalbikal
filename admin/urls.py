from django.urls import path
from .views import VendorListView, VendorDetailsView, VendorStatusUpdateView,\
    ProductDetailsView,CustomerListView,CustomerDetailsView,CustomerStatusUpdateView
urlpatterns = [
    path('admin/vendor/list/', VendorListView.as_view(), name='vendor-list-url'),
    path('admin/vendor/details/<slug>', VendorDetailsView.as_view(), name='vendor-details-url'),
    path('admin/vendor/update/<slug>', VendorStatusUpdateView.as_view(), name='vendor-status-update-url'),
    path('admin/product/details/<slug>', ProductDetailsView.as_view(), name='admin-product-details-url'),
    path('admin/customer/list/', CustomerListView.as_view(), name='customer-list-url'),
    path('admin/customer/details/<slug>', CustomerDetailsView.as_view(), name='customer-details-url'),
    path('admin/customer/update/<slug>', CustomerStatusUpdateView.as_view(), name='customer-status-update-url'),

]
