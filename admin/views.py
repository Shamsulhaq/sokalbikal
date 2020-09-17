from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from product.models import Product
from sokalbikall.permissions_mixin import AdminRequiredMixin
from vendor.models import Vendor
from vendor.forms import VendorStatusUpdateForm
from django.urls import reverse_lazy

class VendorListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = 'admin/vendor/vendor_list.html'
    model = Vendor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Vendor List'
        return context

    def get_queryset(self):
        return Vendor.objects.all()


class VendorDetailsView(LoginRequiredMixin, AdminRequiredMixin, DetailView, FormMixin):
    template_name = 'admin/vendor/vendor_details.html'
    model = Vendor
    form_class = VendorStatusUpdateForm

    def get_context_data(self, **kwargs):
        context = super(VendorDetailsView, self).get_context_data(**kwargs)
        context['product_list'] = Product.objects.get_by_vendor(user=self.object)
        return context


class VendorStatusUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    form_class = VendorStatusUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_context_data(self, **kwargs):
        context = super(VendorStatusUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Vendor Profile Update'
        return context

    def get_queryset(self):
        return Vendor.objects.filter(slug=self.kwargs.get('slug'))

    def get_login_url(self):
        return reverse('login')

    # def get_success_url(self):
    #     return reverse_lazy('vendor-details-url')
