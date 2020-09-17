from django.urls import path

from .views import (
    CustomerProfileUpdateView
)

urlpatterns = [
    path('customer/profile/update/<pk>', CustomerProfileUpdateView.as_view(), name='customer-profile-update'),
    ]
