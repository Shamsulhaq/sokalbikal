from django.db import models
from django.dispatch import receiver
from accounts.models import BaseModels, User
from core.models import Address
from vendor.models import Vendor
from product.models import Product
from sokalbikall.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save


class StatusChoices(models.TextChoices):
    CREATED = "created"
    REJECTED = "rejected"
    PAYMENT_PENDING = "payment pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class ShippingChoices(models.TextChoices):
    HOME_DELIVERY = "home delivery"
    OFFICE_PICK = "office pick"


class Order(BaseModels):
    order_id = models.CharField(max_length=15, blank=True, null=True)
    customer = models.ForeignKey(User, blank=True, null=True,
                                 related_name="order_customer", on_delete=models.DO_NOTHING)
    cart_total = models.DecimalField(default=0.00, decimal_places=5, max_length=9, max_digits=9)
    status = models.CharField(max_length=15, default=StatusChoices.CREATED, choices=StatusChoices.choices)
    reject_reason = models.CharField(max_length=250, blank=True, null=True)
    shipping_method = models.CharField(max_length=15, choices=ShippingChoices.choices,
                                       default=ShippingChoices.HOME_DELIVERY)
    shipping_total = models.DecimalField(default=0.00, decimal_places=5, max_length=9, max_digits=9)
    promo_code = models.CharField(max_length=20, blank=True, null=True)
    discount_amount = models.DecimalField(default=0.00, decimal_places=5, max_length=9, max_digits=9)
    total = models.DecimalField(default=0.00, decimal_places=5, max_length=9, max_digits=9)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", on_delete=models.DO_NOTHING
                                         , blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    # vendor = models.ForeignKey(Vendor, related_name="order_vendor", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.order_id

    def get_shopping_cost(self):
        if self.shipping_method == ShippingChoices.HOME_DELIVERY:
            cost = 50.00
        else:
            cost = 0.00
        return cost

    def update_total_amount(self):
        order_items = Item.objects.filter(order=self.id)
        total = 0
        for item in order_items:
            total += item.item_total
        self.cart_total = total
        self.total = (self.cart_total - self.discount_amount) + self.shipping_total


class Item(models.Model):
    order = models.ForeignKey(Order, related_name="order_item", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_product", on_delete=models.DO_NOTHING)
    price = models.DecimalField(default=0.00, decimal_places=5, max_length=9, max_digits=9)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(default=0.00, decimal_places=5, max_length=9, max_digits=9,
                                     blank=True, null=True)
    status = models.CharField(max_length=15, default=StatusChoices.CREATED, choices=StatusChoices.choices)
    reject_reason = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.item_total:
            self.item_total = self.price * self.quantity
        super(Item, self).save()


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    if instance.shipping_method == ShippingChoices.HOME_DELIVERY:
        instance.shipping_total = instance.get_shopping_cost()


@receiver(post_save, sender =Item)
def item_post_save(sender,instance,created,*args,**kwargs):
    if created:
        if instance.order:
            order_obj = Order.objects.get(id=instance.order.id)
            order_obj.update_total_amount()
            order_obj.save()


