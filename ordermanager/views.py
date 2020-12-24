from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import View
from cart.cart import Cart
from django.contrib.messages.views import messages
from .forms import OrderCreateForms, AddressCreationForms
from core.models import Address, Promo, UserPromoCode
from .models import Order, Item


# Create your views here.


class OrderCreateView(LoginRequiredMixin, View):
    template_name = 'order_create.html'

    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForms()
        address = Address.objects.filter(user=request.user)
        if address:
            form = OrderCreateForms(request.POST, )
        return render(request, self.template_name, {'form': form, 'cart': cart})

    def post(self, request):
        form = OrderCreateForms(request.POST)
        user = request.user
        cart = Cart(request)
        today = timezone.now().date()
        if form.is_valid():
            promo_code = form.cleaned_data['promo_code']
            discount_amount = 0
            if promo_code:
                try:
                    promo = Promo.objects.get(code__icontains=promo_code, is_active=True,
                                              start_date__gte=today, end_date__lte=today)
                except:
                    messages.warning(request, "Wrong or Invalid Promo Code")
                    return redirect('cart-submit-url')
                if promo:
                    print(promo)
                    if promo.max_uses_limit >= promo.use_count:
                        promo_user = UserPromoCode.objects.filter(promo_code=promo, user=user)
                        if not promo_user:
                            if cart.get_total_price() > promo.min_amount:
                                discount_amount = promo.value
                                UserPromoCode.objects.create(promo_code=promo, user=user,
                                                             discounted_amount=discount_amount)
                                promo.use_count += 1
                                promo.save()
                            else:
                                promo_code = ""
                                messages.warning(request, "Your Cart Price Is Low")
                                return redirect('cart-submit-url')
                        else:
                            promo_code = ""
                            messages.warning(request, "You have already Use is Promo code")
                            return redirect('cart-submit-url')
                    else:
                        promo_code = ""
                        messages.warning(request, "This Promo code is Already reach his limit")
                        return redirect('cart-submit-url')

            address = Address.objects.create(user=user, full_name=form.cleaned_data['full_name'],
                                             phone=form.cleaned_data['phone'],
                                             address_line_1=form.cleaned_data['address_line_1'],
                                             city=form.cleaned_data['city'], country=form.cleaned_data['country'],
                                             postal_code=form.cleaned_data['postal_code'])
            order_obj = Order.objects.create(customer=user, shipping_address=address,
                                             shipping_method=form.cleaned_data['shipping_method'],
                                             discount_amount=discount_amount, promo_code=promo_code
                                             )

            if order_obj:
                for item in cart:
                    Item.objects.create(order=order_obj, product=item['product'], price=item['price'],
                                        quantity=item['quantity'])
                cart.clear()
                messages.success(request, "Your Order is placed")
            return redirect('/')
