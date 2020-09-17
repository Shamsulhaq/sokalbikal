from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from sokalbikall.permissions_mixin import VendorRequiredMixin
from vendor.models import Vendor
from .models import Stock
from .forms import ProductCreationFrom


class AllProductView(ListView):
    template_name = 'product_list.html'
    model = Stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products'
        return context

    def get_queryset(self):
        return Stock.objects.all()
