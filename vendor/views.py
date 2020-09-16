from django.shortcuts import render

# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, CreateView, View, ListView, DetailView, UpdateView

from product.models import Product, ProductAttribute,Stock
from .forms import VendorUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from sokalbikall.permissions_mixin import VendorRequiredMixin
from .models import Vendor
from product.forms import ProductCreationFrom, AttributeCreationFrom, StockManageForm


class VendorProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = VendorUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_queryset(self):
        return Vendor.objects.filter(vendor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(VendorProfileUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Profile Update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('profile')


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


class VendorProductListView(LoginRequiredMixin, VendorRequiredMixin, ListView):
    template_name = 'product/product_list.html'
    model = Product
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product List'
        return context

    def get_queryset(self):
        return Product.objects.get_vendor_all_product(self.request.user)


class VendorProductAttributeCreateView(LoginRequiredMixin, VendorRequiredMixin, CreateView):
    template_name = 'add_product.html'
    form_class = AttributeCreationFrom

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        product = Product.objects.get_by_slug(slug)
        instance = form.save(commit=False)
        instance.product = product
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Attribute Create'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('product-attribute-list')


class ProductAttributeListView(LoginRequiredMixin, VendorRequiredMixin, ListView):
    template_name = 'product/attribute_list.html'
    model = ProductAttribute
    context_object_name = 'attribute_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Attribute List'
        return context

    def get_queryset(self):
        return ProductAttribute.objects.get_by_vendor(self.request.user)


class ProductAttributeUpdateView(LoginRequiredMixin, VendorRequiredMixin, UpdateView):
    template_name = 'add_product.html'
    form_class = AttributeCreationFrom

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return ProductAttribute.objects.filter(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Attribute Update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('product-attribute-list')


class StockCreateView(LoginRequiredMixin, VendorRequiredMixin, CreateView):
    template_name = 'add_product.html'
    form_class = StockManageForm

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        product = ProductAttribute.objects.get_by_slug(slug)
        instance = form.save(commit=False)
        instance.product = product
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Stock Manage'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('product-attribute-list')


class ProductStockListView(LoginRequiredMixin, VendorRequiredMixin, ListView):
    template_name = 'product/stock_list.html'
    model = Stock
    context_object_name = 'stock_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Stock List'
        return context

    def get_queryset(self):
        return Stock.objects.get_by_vendor(self.request.user)


class ProductStockUpdateView(LoginRequiredMixin, VendorRequiredMixin, UpdateView):
    template_name = 'add_product.html'
    form_class = StockManageForm

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Stock.objects.filter(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Stock Update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('product-stock-list')
