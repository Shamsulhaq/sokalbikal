import os
import random

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
from accounts.models import User
from vendor.models import Vendor

from django.utils.translation import ugettext_lazy as _
# Create your models here.
from sokalbikall.utils import unique_slug_generator, unique_product_id_generator

fs = FileSystemStorage(location='media')


def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Product image with new name by function
def upload_image_path(inistance, file_name):
    product_name = slugify(inistance.item_name)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"product/{product_name}/{final_filename}"


# ====================+ Product Category Section +============================================
class Category(MPTTModel):
    keyword = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)

    class MPTTMeta:
        order_insertion_by = ['keyword']

    def __str__(self):
        return self.keyword

    @property
    def title(self):
        return self.keyword

    def get_absolute_url(self):
        return reverse('category-details-url', kwargs={"slug": self.slug})

    class Meta:
        verbose_name_plural = 'categories'


# ====================+ Item Section +=======================================================
class ItemQuerySet(models.QuerySet):

    def get_all(self):
        return self.filter(is_active=True)

    def get_vendor_products(self, user):
        return self.filter(creator=user)


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().get_all()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()

    def get_vendor_all_product(self, user):
        return self.get_queryset().get_vendor_products(user=user)


class Item(models.Model):
    item_name = models.CharField(max_length=50, unique=True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                              related_name='product_category')
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    brand = models.CharField(max_length=50)
    creator = models.ForeignKey(Vendor, related_name='product_creator', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    objects = ItemManager()

    def __str__(self):
        return self.item_name

    @property
    def title(self):
        return self.item_name

    def get_absolute_product_attribute_create_url(self):
        return reverse("product-create", kwargs={"slug": self.slug})

    def get_absolute_product_update_url(self):
        return reverse("item-update-url", kwargs={"slug": self.slug})


# ====================+ Product Section +============================================
class ProductQuerySet(models.QuerySet):

    def get_all(self):
        return self.filter(is_active=True)

    def get_active_vendor_all(self):
        return self.filter(item__creator__is_active=True)

    def get_active_all(self):
        return self.filter(item__creator__is_active=True, is_active=True)

    def search(self, keyword):
        lookups = (
                Q(item__item__name__icontains=keyword) |
                Q(item__description__icontains=keyword) |
                Q(item__category__keyword__icontains=keyword) |
                Q(item__brand__icontains=keyword))

        return self.active().filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()

    def get_by_vendor(self, user):
        qs = self.get_queryset().filter(item__creator=user)
        return qs

    def search(self, query):
        return self.get_queryset().search(keyword=query)

    def get_active_vendor_product(self):
        return self.get_queryset().get_active_vendor_all()

    def get_active_all(self):
        return self.get_queryset().get_active_all()


class Product(models.Model):
    product_id = models.PositiveIntegerField(unique=True, blank=True)
    size = models.CharField(max_length=220)
    quantity = models.PositiveIntegerField()
    regular_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    item = models.ForeignKey(Item, related_name='product_size', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_return = models.BooleanField(_('Accept our Return Policy'), default=False, )
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    objects = ProductManager()

    def __str__(self):
        return "{product} -> {size}".format(product=self.item, size=self.size)

    @property
    def title(self):
        return self.item.item_name + self.size

    def get_absolute_vendor_product_details_url(self):
        return reverse("vendor-product-details", kwargs={"slug": self.slug})

    def get_absolute_vendor_product_status_update_url(self):
        return reverse("admin-product-status-update-url", kwargs={"slug": self.slug})

    def get_absolute_admin_product_details_url(self):
        return reverse("admin-product-details-url", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        return reverse("product-update", kwargs={"slug": self.slug})

    def get_absolute_public_product_details_url(self):
        return reverse("customer-product-details-url", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return reverse("admin-product-details-url", kwargs={"slug": self.slug})


# ======================+ Stock Section +==========================================
# class StockQuerySet(models.QuerySet):
#
#     def get_all(self):
#         return self.filter(is_active=True)
#
#
# class StockManager(models.Manager):
#     def get_queryset(self):
#         return StockQuerySet(self.model, using=self._db)
#
#     def all(self):
#         return self.get_queryset().get_all()
#
#     def get_by_slug(self, slug):
#         qs = self.get_queryset().filter(slug=slug)
#         if qs.count() == 1:
#             return qs.first()
#
#     def get_by_vendor(self, user):
#         qs = self.get_queryset().get_all().filter(product__item__creator=user)
#         return qs
#
#
# class Stock(models.Model):
#     quantity = models.PositiveIntegerField()
#     product = models.ForeignKey(Product, related_name='stock_product', on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     last_update = models.DateTimeField(auto_now=True)
#     slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
#     objects = StockManager()
#
#     def __str__(self):
#         return "{vendor} -> {product}".format(vendor=self.product.item.creator, product=self.product)
#
#     @property
#     def title(self):
#         return self.product.item.product_name
#
#     def get_absolute_stock_update_url(self):
#         return reverse("product-stock-update", kwargs={"slug": self.slug})
#

# +============================== Signals +===========================================

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(category_pre_save_receiver, sender=Category)


def item_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(item_pre_save_receiver, sender=Item)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if not instance.product_id:
        instance.product_id = unique_product_id_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)

# def stock_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#
#
# pre_save.connect(stock_pre_save_receiver, sender=Product)


# def attribute_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         Stock.objects.get_or_create(product=instance, quantity=0)
#
#
# post_save.connect(attribute_created_receiver, sender=Product)
