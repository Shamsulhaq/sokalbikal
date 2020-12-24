from django.contrib import admin
from .models import Address, Promo, UserPromoCode

# Register your models here.
admin.site.register(Address)
admin.site.register(Promo)
admin.site.register(UserPromoCode)
