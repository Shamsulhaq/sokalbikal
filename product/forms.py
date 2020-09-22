from django import forms

from .models import Category, Item, Product


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'keyword',
            'parent'
        ]
        labels = {
            'keyword': 'Category',
            'parent': 'Main Category'
        }


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


class ProductStatusUpdateFrom(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'is_active'
        ]
