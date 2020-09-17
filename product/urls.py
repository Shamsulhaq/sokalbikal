from django.urls import path
from .views import AllProductView

urlpatterns = [
    path('product/list/', AllProductView.as_view(), name='product-list'),
    # path('product/update/<slug>', ProductUpdateView.as_view(), name='product-update-url'),
]
