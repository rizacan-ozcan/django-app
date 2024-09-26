import re
from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.filter(name="strip_html")
def strip_html(value):
    return strip_tags(value)