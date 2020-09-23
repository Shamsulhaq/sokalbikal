from django.conf import settings
from django.db import models
from product.models import Product


User = settings.AUTH_USER_MODEL

# Create your models here.

# class Order(models.Model):
#     order_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
#     customer = models.ForeignKey(User,related_name='order_customer',on_delete=models.CASCADE, blank=True, null=True)
#
