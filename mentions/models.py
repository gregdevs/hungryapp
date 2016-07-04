from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

    for user in User.objects.all():
        Token.objects.get_or_create(user=user)

class Mention(models.Model):
    author = models.ForeignKey(User)
    placeid = models.ForeignKey('places.Place', null=True)
    placeinfo = models.ForeignKey('places.Place', related_name='placeinfo', null=True)
    username =  models.CharField(max_length=140, default='Username')
    placemention = models.TextField(max_length=140, default='SOME STRING')
    lat = models.DecimalField(max_digits=20, decimal_places=15)
    lng = models.DecimalField(max_digits=20, decimal_places=15)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.placemention


class Hashtag(models.Model):
    mention = models.ForeignKey(Mention, related_name='hashtags')
    tagname = models.CharField(max_length=100)

    class Meta:
        unique_together = ('mention', 'tagname')

    def __unicode__(self):
        return '%s' % (self.tagname)
     



