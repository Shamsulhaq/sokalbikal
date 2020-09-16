from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from sokalbikall.permissions_mixin import VendorRequiredMixin
from vendor.models import Vendor
from .models import Product
from .forms import ProductCreationFrom


class CreateProductView(LoginRequiredMixin, VendorRequiredMixin, CreateView):
    template_name = 'add_product.html'
    form_class = ProductCreationFrom

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Create'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('index')


class ProductUpdateView(LoginRequiredMixin, VendorRequiredMixin, UpdateView):
    template_name = 'add_product.html'
    form_class = ProductCreationFrom

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Product.objects.filter(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('vendor-product-list')
