from django import forms

from .models import Product, ProductAttribute, Stock


class ProductCreationFrom(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'category',
            'description',
            'image',
            'brand',
        ]


class AttributeCreationFrom(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = [
            'size',
            'regular_price',
            'price',
        ]


class StockManageForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            'quantity',
        ]
