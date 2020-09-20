from django import forms
from django.contrib.auth import get_user_model
from django.contrib.messages.views import messages
from .models import Customer

User = get_user_model()


# Create your form here.
class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'image',
            'date_of_birth',
            'address'
        )
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class CustomerStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'is_active',
        )
        labels = {
            'is_active': 'Are You Agree to Verified'
        }
