from django.shortcuts import render

# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, CreateView, View, ListView, DetailView, UpdateView

from product.models import Item, Product
from .forms import VendorUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from sokalbikall.permissions_mixin import VendorRequiredMixin
from .models import Vendor
from product.forms import ItemCreationFrom, ProductCreationFrom


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


class ItemCreateView(LoginRequiredMixin, VendorRequiredMixin, CreateView):
    template_name = 'add_product.html'
    form_class = ItemCreationFrom

    def form_valid(self, form):
        instance = form.save(commit=False)
        vendor = Vendor.objects.get(vendor=self.request.user)
        instance.creator = vendor
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Item Create'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('vendor-item-list')


class ItemUpdateView(LoginRequiredMixin, VendorRequiredMixin, UpdateView):
    template_name = 'add_product.html'
    form_class = ItemCreationFrom

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        vendor = Vendor.objects.get(vendor=self.request.user)
        return Item.objects.filter(slug=slug, creator=vendor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Item Update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('vendor-item-list')


class VendorItemListView(LoginRequiredMixin, VendorRequiredMixin, ListView):
    template_name = 'product/item_list.html'
    model = Item
    context_object_name = 'item_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Item List'
        return context

    def get_queryset(self):
        vendor = Vendor.objects.get(vendor=self.request.user)
        return Item.objects.get_vendor_all_product(user=vendor)


class ProductCreateView(LoginRequiredMixin, VendorRequiredMixin, CreateView):
    template_name = 'add_product.html'
    form_class = ProductCreationFrom

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        vendor = Vendor.objects.get(vendor=self.request.user)
        product = Item.objects.get(slug=slug, creator=vendor)
        instance = form.save(commit=False)
        instance.item = product
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Create'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('vendor-product-list')


class ProductListView(LoginRequiredMixin, VendorRequiredMixin, ListView):
    template_name = 'product/product_list.html'
    model = Product
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product List'
        return context

    def get_queryset(self):
        vendor = Vendor.objects.get(vendor=self.request.user)
        return Product.objects.get_by_vendor(user=vendor)


class ProductUpdateView(LoginRequiredMixin, VendorRequiredMixin, UpdateView):
    template_name = 'add_product.html'
    form_class = ProductCreationFrom

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        vendor = Vendor.objects.get(vendor=self.request.user)
        return Product.objects.filter(slug=slug, item__creator=vendor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('vendor-product-list')


class ProductDetailsView(LoginRequiredMixin,VendorRequiredMixin, DetailView):
    template_name = 'product/product_details.html'
    model = Product


