from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.urlresolvers import reverse
from bbsittingsharing import settings

class BBSitting(models.Model):
   date = models.DateField()
   start = models.TimeField()
   bbsitter_found = models.BooleanField()
   children_capacity = models.IntegerField()
   author = models.ForeignKey(settings.AUTH_USER_MODEL)
   
   def get_absolute_url(self):
       return reverse('detail', args=[str(self.id)])
       
   def __unicode__(self):
      return "At %s's on %s"%(self.author, self.date)

class Parent(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
