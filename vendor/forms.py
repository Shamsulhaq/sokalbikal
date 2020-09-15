from django import forms
from django.contrib.auth import get_user_model
from django.contrib.messages.views import messages
from .models import Vendor

User = get_user_model()


# Create your form here.
class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = (
            'shop_name',
            'shop_location',
            'description',
            'image'
        )

