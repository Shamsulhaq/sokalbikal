from django.urls import path

from .views import (
    VendorProfileUpdateView
)

urlpatterns = [
    path('vendor/profile/update/<slug>', VendorProfileUpdateView.as_view(), name='vendor-profile-update'),
]
