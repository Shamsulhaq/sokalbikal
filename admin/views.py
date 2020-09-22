from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin, messages

from accounts.models import User
from customer.models import Customer
from customer.forms import CustomerStatusUpdateForm
from product.models import Product, Category
from product.forms import CategoryCreationForm, ProductStatusUpdateFrom
from sokalbikall.permissions_mixin import AdminRequiredMixin
from vendor.models import Vendor
from vendor.forms import VendorStatusUpdateForm
from django.urls import reverse_lazy


class CategoryView(SuccessMessageMixin, LoginRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = 'admin/product/category/category_view.html'
    form_class = CategoryCreationForm
    success_message = 'Category Create Successful.'

    def form_valid(self, form):
        instance = form.save(commit=False)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Category.objects.all()
        context['title'] = 'Category'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse_lazy('category-view-url')


class CategoryDetailsView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    template_name = 'admin/product/category/category_detail.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cats = []
        obj = context['object']
        if obj.level == 0:
            cats.append(('Category', obj.title))
        else:
            for x in range(obj.level + 1, 0, -1):
                if x == 1:
                    sub = ''
                else:
                    sub = 'Sub ' * (x - 1)
                cats.append((sub + 'Category', obj.title))
                obj = obj.parent
        cats.reverse()
        context['categories'] = cats
        return context


class ProductDetailsView(LoginRequiredMixin, AdminRequiredMixin, DetailView, FormMixin):
    template_name = 'admin/vendor/product_details.html'
    model = Product
    form_class = ProductStatusUpdateFrom


class ProductStatusUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    form_class = ProductStatusUpdateFrom
    template_name = 'accounts/profile_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product Status Update'
        return context

    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs.get('slug'))

    def get_login_url(self):
        return reverse('login')

    # def get_success_url(self):
    #     return reverse_lazy('admin-product-details-url',slug=self.kwargs.get('slug'))


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


class CustomerListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = 'admin/customer/customer_list.html'
    model = Customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Customer List'
        return context

    def get_queryset(self):
        return Customer.objects.all()


class CustomerDetailsView(LoginRequiredMixin, AdminRequiredMixin, DetailView, FormMixin):
    template_name = 'admin/customer/customer_details.html'
    model = Customer
    form_class = CustomerStatusUpdateForm

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailsView, self).get_context_data(**kwargs)
        # context['product_list'] = Product.objects.get_by_vendor(user=self.object)
        return context


class CustomerStatusUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    form_class = CustomerStatusUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerStatusUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Customer Profile Update'
        return context

    def get_queryset(self):
        return Customer.objects.filter(slug=self.kwargs.get('slug'))

    def get_login_url(self):
        return reverse('login')


class AllUserList(ListView):
    model = User
    template_name = 'admin/user/user_list.html'

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User List'
        return context
