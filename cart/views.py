from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.http import is_safe_url
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import FormMixin

from product.models import Product
from .forms import CartAddProductForm
from .cart import Cart


# class CartCreateView(FormView):
#     template_name = 'temporary/product_list.html'
#     form_class = CartAddProductForm
#     success_message = 'Cart Add Successful.'
#
#     def form_valid(self, form):
#         cart = Cart(self.request)
#         product = Product.objects.get_by_slug(self.kwargs.get('slug'))
#         cd = form.cleaned_data
#         cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
#         return HttpResponse(str(reverse('product-home-url')))
#
#     def get_login_url(self):
#         return reverse('login')
#
#     def get_success_url(self):
#         return reverse('product-home-url')


@require_POST
def cart_add(request, pk):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    cart = Cart(request)  # create a new cart object passing it the request object
    product = get_object_or_404(Product, pk=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        print(cd)
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/')
    return redirect('product-home-url')


class CartListView(ListView):
    template_name = 'cart_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for item in Cart(self.request):
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        return context

    def get_queryset(self):
        return Cart(self.request)


def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove(product)
    return redirect('cart-list-url')
