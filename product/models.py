import os
import random

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

from accounts.models import User
from vendor.models import Vendor

# Create your models here.
from sokalbikall.utils import unique_slug_generator, unique_product_id_generator

fs = FileSystemStorage(location='media')


def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Product image with new name by function
def upload_image_path(inistance, file_name):
    product_name = slugify(inistance.product_name)
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

    class Meta:
        verbose_name_plural = 'categories'


# ====================+ Product Section +=======================================================
class ProductQuerySet(models.QuerySet):

    def get_all(self):
        return self.filter(is_active=True)

    def get_vendor_products(self, user):
        return self.filter(creator=user)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().get_all()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()

    def get_vendor_all_product(self, user):
        return self.get_queryset().get_vendor_products(user=user)


class Product(models.Model):
    product_id = models.PositiveIntegerField(unique=True, blank=True)
    product_name = models.CharField(max_length=50, unique=True)
    category = TreeForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                              related_name='product_category')
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    brand = models.CharField(max_length=50)
    # regular_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, blank=True, null=True)
    # price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    # in_stock = models.PositiveIntegerField()
    creator = models.ForeignKey(User, related_name='product_creator', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    objects = ProductManager()

    class Meta:
        unique_together = ["product_id", "product_name"]

    def __str__(self):
        return self.product_name

    @property
    def title(self):
        return self.product_name

    def get_absolute_product_attribute_create_url(self):
        return reverse("product-attribute-create", kwargs={"slug": self.slug})

    def get_absolute_product_update_url(self):
        return reverse("product-update-url", kwargs={"slug": self.slug})


# ====================+ Product Attribute Section +============================================
class AttributeQuerySet(models.QuerySet):

    def get_all(self):
        return self.filter(is_active=True)

    # def get_by_vendor(self,user):
    #     return self.filter(product.creator = user)


class AttributeManager(models.Manager):
    def get_queryset(self):
        return AttributeQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().get_all()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()

    def get_by_vendor(self, user):
        qs = self.get_queryset().filter(product__creator=user)
        return qs


class ProductAttribute(models.Model):
    size = models.FloatField()
    regular_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    product = models.ForeignKey(Product, related_name='product_size', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    objects = AttributeManager()

    def __str__(self):
        return "{product} -> {size}".format(product=self.product, size=self.size)

    @property
    def title(self):
        return self.product.product_name


class Stock(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(ProductAttribute, related_name='stock_product', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{vendor} -> {product}".format(vendor=self.product.product.creator, product=self.product)


# +============================== Signals +===========================================

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(category_pre_save_receiver, sender=Category)


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.product_id:
        instance.product_id = unique_product_id_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def attribute_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(attribute_pre_save_receiver, sender=ProductAttribute)
