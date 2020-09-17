from django.urls import path
from .views import VendorListView, VendorDetailsView, VendorStatusUpdateView
urlpatterns = [
    path('admin/vendor/list/', VendorListView.as_view(), name='vendor-list-url'),
    path('admin/vendor/details/<slug>', VendorDetailsView.as_view(), name='vendor-details-url'),
    path('admin/vendor/update/<slug>', VendorStatusUpdateView.as_view(), name='vendor-status-update-url'),
]
