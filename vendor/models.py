import os
import random

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify

from accounts.models import User
from sokalbikall.utils import unique_slug_generator

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


# Create your models here.
class Vendor(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_rl')
    shop_name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    description = models.TextField(blank=True)
    shop_location = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)

    def __str__(self):
        return str(self.vendor)

    @property
    def title(self):
        return self.shop_name


def vendor_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.shop_name:
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)


pre_save.connect(vendor_pre_save_receiver, sender=Vendor)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.role == 'vendor':
        Vendor.objects.get_or_create(vendor=instance)


post_save.connect(user_created_receiver, sender=User)
