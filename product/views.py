from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from cart.forms import CartAddProductForm
from sokalbikall.permissions_mixin import VendorRequiredMixin
from vendor.models import Vendor
from .models import Product
from .forms import ItemCreationFrom


# +========================= ADMIN SIDE+=========================================
class AllProductView(ListView):
    template_name = 'product_list.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Product'
        return context

    def get_queryset(self):
        return Product.objects.all()


class AllActiveProductList(ListView):
    template_name = 'product_list.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active Products'
        return context

    def get_queryset(self):
        return Product.objects.get_active_vendor_product()


# ===========================+++++====================================================
# ==============================+ Client Side +=======================================

class PubProductListView(ListView, FormMixin):
    template_name = 'temporary/product_list.html'
    model = Product
    form_class = CartAddProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active Products'
        return context

    def get_queryset(self):
        return Product.objects.get_active_all()


class PubProductDetailsView(DetailView):
    template_name = 'temporary/product_details.html'
    model = Product
