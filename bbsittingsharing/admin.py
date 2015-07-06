from django.contrib import admin
from django.utils.translation import ugettext as _
from bbsittingsharing.models import *
from bbsittingsharing.helpers import send_email

def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)
    recipients = [user.email for user in queryset.all()]
    send_email(recipients, _("BBSitting sharing: Account validated"), "account_validated")
activate.short_description = _("Activate users")

class ParentAdmin(admin.ModelAdmin):
    list_display = ('email', 'referer', 'district', 'is_active')
    actions = [activate]

admin.site.register(District)
admin.site.register(School)
admin.site.register(Parent, ParentAdmin)
admin.site.register(BBSitting)
admin.site.register(Booking)
admin.site.register(Equipment)
