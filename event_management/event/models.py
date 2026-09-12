from django.db import models
from django_cleanup import cleanup
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
    price = models.IntegerField()
    Image = models.ImageField()
    
    
    def __str__(self):
        return self.title