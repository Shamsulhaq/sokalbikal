from django import forms

from .models import Item, Product


class ItemCreationFrom(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_name',
            'category',
            'description',
            'image',
            'brand',
        ]


class ProductCreationFrom(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'size',
            'quantity',
            'regular_price',
            'price',
            'is_return'
        ]



