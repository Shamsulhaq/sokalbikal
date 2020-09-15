from django.contrib import admin
from product.models import Product,ProductAttribute,Category,Stock
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(Stock)