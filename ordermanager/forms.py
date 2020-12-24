from django import forms
from .models import Address,Order, ShippingChoices

class AddressCreationForms(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'full_name', 'phone', 'address_line_1', 'city', 'country', 'postal_code'
        )


SHIPPING_CHOICE = (
    ("office pick", "Office Pick"),
    ("home delivery", "Home Delivery")
)


class OrderCreateForms(forms.Form):
    shipping_method = forms.ChoiceField(choices=SHIPPING_CHOICE)
    full_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=15, required=True)
    address_line_1 = forms.CharField(max_length=250, required=True)
    city = forms.CharField(max_length=250, required=True)
    country = forms.CharField(max_length=250, required=True)
    postal_code = forms.CharField(max_length=250, required=True)
    promo_code = forms.CharField(max_length=20, required=False)