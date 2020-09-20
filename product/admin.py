from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from product.models import Item,Product,Category
# Register your models here.
admin.site.register(Category,MPTTModelAdmin)
admin.site.register(Item)
admin.site.register(Product)