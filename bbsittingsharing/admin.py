from django.contrib import admin
from django.utils.translation import ugettext as _
from bbsittingsharing.models import *

def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate.short_description = _("Activate users")

class ParentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'referer', 'district', 'is_active')
    actions = [activate]

admin.site.register(District)
admin.site.register(Parent, ParentAdmin)
admin.site.register(BBSitting)
admin.site.register(Booking)
admin.site.register(Equipment)
