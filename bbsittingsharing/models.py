from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class BBSitting(models.Model):
   date = models.DateField()
   start = models.TimeField()
   bbsitter_found = models.BooleanField()
   children_capacity = models.IntegerField()
   author = models.ForeignKey(User)
   
   def get_absolute_url(self):
       return reverse('detail', args=[str(self.id)])
       
   def __unicode__(self):
      return "At %s's on %s"%(self.author, self.date)
