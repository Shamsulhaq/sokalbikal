from django.db import models

# Create your models here.
from django.utils import timezone

from accounts.models import User,BaseModels,UnitOfHistory
from vendor.models import Vendor


class Promo(BaseModels):
    code = models.CharField(max_length=20)
    max_uses_limit = models.IntegerField()
    max_limit_per_user = models.IntegerField(default=1)
    value = models.IntegerField()
    min_amount = models.IntegerField(default=0)
    creator = models.ForeignKey(Vendor, related_name="promo_creator", blank=True,
                                null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    use_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Code: {self.code} Amount: {self.min_amount}"


class Address(BaseModels):
    user = models.ForeignKey(User, related_name="customer_address", on_delete=models.DO_NOTHING)
    full_name = models.CharField(max_length=155)
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=120)
    city = models.CharField(max_length=120, default='Dhaka')
    country = models.CharField(max_length=120, default='Bangladesh')
    postal_code = models.CharField(max_length=120)


class UserPromoCode(BaseModels):
    promo_code = models.ForeignKey(Promo, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="used_promo_codes"
    )
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_payment_success = models.BooleanField(default=False)