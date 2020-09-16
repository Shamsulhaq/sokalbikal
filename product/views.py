from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from sokalbikall.permissions_mixin import VendorRequiredMixin
from vendor.models import Vendor
from .models import Product
from .forms import ProductCreationFrom


