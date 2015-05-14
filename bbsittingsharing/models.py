from os.path import splitext
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.urlresolvers import reverse
from bbsittingsharing import settings

class BBSitting(models.Model):
   date             = models.DateField()
   start            = models.TimeField()
   bbsitter_found   = models.BooleanField()
   children_capacity= models.IntegerField()
   author           = models.ForeignKey(settings.AUTH_USER_MODEL)
   booked           = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Booking', related_name="booked")
   
   def get_absolute_url(self):
       return reverse('detail', args=[str(self.id)])
       
   def __unicode__(self):
      return "At %s's on %s"%(self.author, self.date)

class Parent(AbstractUser):
    phone       = models.CharField(max_length=20, blank=True, null=True)
    kidsnb      = models.IntegerField(blank=True, null=True)
    school      = models.CharField(max_length=255, blank=True, null=True)
    bbsitter    = models.CharField(max_length=255, blank=True, null=True)
    ok_at_home  = models.BooleanField(default=True)
    ok_at_others= models.BooleanField(default=True)
    
    def picture_name(self, filename):
        """Generates the picture filename from the username"""
        return '%s%s'%(self.username, splitext(filename)[1])
    picture     = models.ImageField(upload_to=picture_name, default="/static/user.jpg")
    
    def __unicode__(self):
        return "%s's profile"%(self.get_full_name())

class Booking(models.Model):
    parent = models.ForeignKey(Parent)
    bbsitting = models.ForeignKey(BBSitting)
    confirmed = models.BooleanField(default=False)
    class Meta:
       unique_together = ("parent", "bbsitting")
    def __unicode__(self):
        return "%s's booking for %s"%(self.parent, self.bbsitter)
