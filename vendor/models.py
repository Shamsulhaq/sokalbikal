import os
import random

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
from django.urls import reverse

from accounts.models import User
from sokalbikall.utils import unique_slug_generator

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

fs = FileSystemStorage(location='media')


def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Author image with new name by function
def upload_image_path(inistance, file_name):
    vendor_name = slugify(inistance.shop_name)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"vendor/{vendor_name}/{final_filename}"


def upload_trade_path(inistance, file_name):
    vendor_name = slugify(inistance.shop_name)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"vendor/trade/{vendor_name}/{final_filename}"


class VendorQuerySet(models.QuerySet):

    def get_verified_all(self):
        return self.filter(is_active=True)


class VendorManager(models.Manager):
    def get_queryset(self):
        return VendorQuerySet(self.model, using=self._db)

    def verified_all(self):
        return self.get_queryset().get_verified_all()

    def all(self):
        return self.get_queryset().all()


# Create your models here.
SHOP_TYPE = (('virtual', 'Virtual'),
             ('existent', 'Existent '))


class Vendor(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_rl')
    shop_name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    description = models.TextField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    help_line = models.CharField(_('help line number'), validators=[phone_regex], max_length=15, unique=True, blank=True)
    shop_location = models.CharField(max_length=250)
    shop_type = models.CharField(choices=SHOP_TYPE, max_length=20)
    trade_licence = models.ImageField(upload_to=upload_trade_path, blank=True)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    objects = VendorManager()

    def __str__(self):
        return str(self.shop_name)

    @property
    def title(self):
        return self.shop_name

    def is_verified(self):
        return self.is_active

    def get_absolute_update_url(self):
        return reverse("vendor-profile-update", kwargs={"pk": self.pk})


def vendor_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.shop_name:
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)


pre_save.connect(vendor_pre_save_receiver, sender=Vendor)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.role == 'vendor':
        Vendor.objects.get_or_create(vendor=instance)


post_save.connect(user_created_receiver, sender=User)
