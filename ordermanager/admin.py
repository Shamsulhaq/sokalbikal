from django.contrib import admin
from .models import Item, Order
# Register your models here.


class ItemAdmin(admin.StackedInline):
    model = Item


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemAdmin]

    class Meta:
        model = Order

# admin.site.register(Address)
