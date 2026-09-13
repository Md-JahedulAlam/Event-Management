from django.db import models
from django_cleanup import cleanup
# from django.contrib.auth.models import User
from accounts.models import User
import os
# Create your models here.
def Image_path(instance, filename):
    extention = filename.split('.')[-1]
    filename=f"{instance.title}-{instance.event_date}.{extention}"
    return os.path.join('Events',filename)


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
@cleanup.select
class Events(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    locations = models.CharField(max_length=150)
    event_date = models.DateField()
    event_time = models.TimeField()
    total_sets = models.IntegerField()
    available_sets = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Image = models.ImageField(upload_to=Image_path,blank=True, null=True)
    
    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    number_of_tickets = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)