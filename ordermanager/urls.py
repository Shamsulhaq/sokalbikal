from django.urls import path
from .views import OrderCreateView

urlpatterns = [
    path('product/checkout/', OrderCreateView.as_view(), name='cart-submit-url'),
]
