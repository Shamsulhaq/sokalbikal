import os
import random

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify

from accounts.models import User

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
class Customer(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_user')
    date_of_birth = models.DateField()
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    address = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.person.first_name)

    @property
    def title(self):
        return self.person.first_name


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.role == 'customer':
        Customer.objects.get_or_create(person=instance)


post_save.connect(user_created_receiver, sender=User)
