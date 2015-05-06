from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def bbjson(value):
    """turns a bbsitting list into json"""
    json_data = '{"title":"At %s\'s", "start":"%s", "url": "%s"}'
    bbjson_list = map(lambda bb: json_data%(bb.author, bb.date, reverse("detail", kwargs={'pk':bb.pk})), value)
    return mark_safe("[%s]"%(",".join(bbjson_list)))
