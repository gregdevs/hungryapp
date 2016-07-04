from django.db import models 
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Friend(models.Model):
    username = models.CharField(max_length=140, default='SOME STRING')
    friendswith = models.ForeignKey(User)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
     
    def __unicode__(self):
        return self.username        