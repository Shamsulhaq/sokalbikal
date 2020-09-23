import os
import random

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
from django.urls import reverse

from accounts.models import User
from sokalbikall.utils import unique_slug_generator

fs = FileSystemStorage(location='media')


def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Author image with new name by function
def upload_image_path(inistance, file_name):
    customer_name = slugify(inistance.person)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"customer/{customer_name}/{final_filename}"


# Create your models here.
class CustomerQuerySet(models.QuerySet):

    def get_all(self):
        return self.filter(is_active=True)


class CustomerManager(models.Manager):
    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()


CHOOSE_GENDER = (('male', 'Male'), ('female', 'Female'))


class Customer(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_user')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=CHOOSE_GENDER, blank=True, null=True,max_length=30)
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    address = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    objects = CustomerManager()

    def __str__(self):
        return str(self.person.first_name)

    @property
    def title(self):
        return self.person.first_name + " " + self.person.last_name

    def get_absolute_url(self):
        return reverse('customer-details-url', kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        return reverse("customer-profile-update", kwargs={"pk": self.pk})

    def get_absolute_status_url(self):
        return reverse('customer-status-update-url', kwargs={'slug': self.slug})

    # def get_absolute_delete_url(self):
    #     return reverse("delete-post", kwargs={"slug": self.slug})


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.role == 'customer':
        Customer.objects.get_or_create(person=instance)


post_save.connect(user_created_receiver, sender=User)


def customer_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(customer_pre_save_receiver, sender=Customer)
