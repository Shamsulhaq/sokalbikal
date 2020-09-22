from django.urls import path
from .views import (CategoryView, CategoryDetailsView, ProductDetailsView, ProductStatusUpdateView, VendorListView,
                    VendorDetailsView, VendorStatusUpdateView, CustomerListView, CustomerDetailsView,
                    CustomerStatusUpdateView,AllUserList)

urlpatterns = [
    path('admin/category/list/', CategoryView.as_view(), name='category-view-url'),
    path('admin/category/details/<slug>', CategoryDetailsView.as_view(), name='category-details-url'),
    path('admin/product/details/<slug>', ProductDetailsView.as_view(), name='admin-product-details-url'),
    path('admin/product/update/<slug>', ProductStatusUpdateView.as_view(),
         name='admin-product-status-update-url'),
    path('admin/vendor/list/', VendorListView.as_view(), name='vendor-list-url'),
    path('admin/vendor/details/<slug>', VendorDetailsView.as_view(), name='vendor-details-url'),
    path('admin/vendor/update/<slug>', VendorStatusUpdateView.as_view(), name='vendor-status-update-url'),
    path('admin/customer/list/', CustomerListView.as_view(), name='customer-list-url'),
    path('admin/customer/details/<slug>', CustomerDetailsView.as_view(), name='customer-details-url'),
    path('admin/customer/update/<slug>', CustomerStatusUpdateView.as_view(), name='customer-status-update-url'),
    path('admin/user/list/',AllUserList.as_view(),name='all-user-url')

]
