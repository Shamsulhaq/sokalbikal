from django import forms
from django.contrib.auth import get_user_model
from django.contrib.messages.views import messages
from .models import Vendor

User = get_user_model()


# Create your form here.
class VendorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = (
            'shop_name',
            'shop_location',
            'description',
            'image'
        )

    def save(self, commit=True):
        vendor = super(VendorRegistrationForm, self).save(commit=False)
        vendor.is_active = False
        if commit:
            self.save()


class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = (
            'shop_name',
            'shop_location',
            'description',
            'image'
        )
