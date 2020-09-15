from django.shortcuts import render

# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, CreateView, View, TemplateView, DetailView,UpdateView
from .forms import VendorUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Vendor


class VendorProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = VendorUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_queryset(self):
        return Vendor.objects.filter(vendor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(VendorProfileUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Vendor Profile Update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('profile')
