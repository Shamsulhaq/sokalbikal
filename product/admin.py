from django.contrib import admin
from product.models import Item,Product,Category
# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Product)