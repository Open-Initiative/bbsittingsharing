from os.path import splitext
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from bbsittingsharing import settings

class BBSitting(models.Model):
   date             = models.DateField(verbose_name=_("Date"))
   start            = models.TimeField(verbose_name=_("Start"))
   bbsitter_found   = models.BooleanField(verbose_name=_("Have you found a bbsitter?"))
   at_authors       = models.BooleanField(verbose_name=_("Would you rather have the bbsitting at your place?"))
   authors_children = models.IntegerField(verbose_name=_("How many children will be present on your side?"))
   children_capacity= models.IntegerField(verbose_name=_("How many children will you share this bbsitting with at most?"))
   author           = models.ForeignKey(settings.AUTH_USER_MODEL)
   booked           = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Booking', related_name="booked")
   
   def get_absolute_url(self):
       return reverse('detail', args=[str(self.id)])
       
   def __unicode__(self):
      return _("At %(author)s's on %(date)s %(with)s babysitter")%{'author':self.author.get_full_name(), 'date':self.date, 'with': 'with' if self.bbsitter_found else 'without'}


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    default = models.BooleanField()
    def __unicode__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group)
    def __unicode__(self):
        return self.name

class Parent(AbstractUser):
    phone       = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone number"))
    kidsnb      = models.IntegerField(blank=True, null=True, verbose_name=_("Number of kids"))
    school      = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("School name"))
    bbsitter    = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Usual bbsitter"))
    ok_at_home  = models.BooleanField(default=True, verbose_name="Ok "+_("to host a bbsitting"))
    ok_at_others= models.BooleanField(default=True, verbose_name="Ok "+_("to go to someone else's place"))
    friends     = models.ManyToManyField("self", blank=True, null=True)
    referer     = models.ForeignKey("self", related_name="referees", blank=True, null=True, verbose_name=_("Referer"))
    district    = models.ForeignKey(District, related_name="users", null=True, verbose_name=_("District"))
    equipment   = models.ManyToManyField(Equipment, blank=True, verbose_name=_("Equipment"))
    
    def picture_name(self, filename):
        """Generates the picture filename from the username"""
        return '%s%s'%(self.username, splitext(filename)[1])
    picture     = models.ImageField(upload_to=picture_name, default="/static/user.png")
    
    def shared_nb(self):
        """Gets the number of babysittings the user has proposed and booked"""
        return self.bbsitting_set.count() + self.booked.count()
    
    def get_full_name(self):
        return super(Parent, self).get_full_name() or self.username
    
    def __unicode__(self):
        return self.get_full_name()

class Booking(models.Model):
    parent = models.ForeignKey(Parent)
    bbsitting = models.ForeignKey(BBSitting)
    confirmed = models.BooleanField(default=False)
    class Meta:
       unique_together = ("parent", "bbsitting")
    def __unicode__(self):
        return _("%(parent)s's booking for %(bbsitting)s"%{'parent':self.parent, 'bbsitting':self.bbsitting})
