from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Place(models.Model):
    placename = models.CharField(max_length=140, default='placename')
    placecity = models.CharField(max_length=100, default='somecity')
    lat = models.DecimalField(max_digits=20, decimal_places=10)
    lng = models.DecimalField(max_digits=20, decimal_places=10)    
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.placename