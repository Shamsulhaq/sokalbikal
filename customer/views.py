from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, CreateView, View, TemplateView, DetailView, UpdateView
from .forms import CustomerRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Customer


class CustomerProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CustomerRegistrationForm
    template_name = 'accounts/profile_update.html'

    def get_queryset(self):
        return Customer.objects.filter(person=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CustomerProfileUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Profile Update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('profile')
