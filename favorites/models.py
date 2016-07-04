from django.db import models 
from django.utils import timezone
from django.contrib.auth.models import User
from places.models import Place
# Create your models here.

class Favorite(models.Model):
	placename = models.CharField(max_length=200, default="some place")
	placeid = models.ForeignKey(Place, null=True)
	userid =  models.ForeignKey(User)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save() 

	def __unicode__(self):
		return self.placename