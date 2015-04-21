from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def bbjson(value):
    """turns a bbsitting list into json"""
    bbjson_list = map(lambda bb: '{"title":"At %s\'s", "start":"%s"}'%(bb.author, bb.date), value)
    return mark_safe("[%s]"%(",".join(bbjson_list)))
