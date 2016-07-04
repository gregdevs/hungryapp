from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from mentions.models import Mention
defaultval = 1

class Reputation(models.Model):
    author = models.ForeignKey(User)
    authorname =  models.CharField(max_length=140, default='Authorname')
    mention = models.ForeignKey(Mention, null=True)
    placeid = models.ForeignKey('places.Place', null=True)
    value = models.IntegerField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.authorname


     



