from django.urls import path
from .views import CreateProductView,ProductUpdateView


urlpatterns = [
    path('product/create', CreateProductView.as_view(), name='product-create-url'),
    path('product/update/<slug>', ProductUpdateView.as_view(), name='product-update-url'),
]
