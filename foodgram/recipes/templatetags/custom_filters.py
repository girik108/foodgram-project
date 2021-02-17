from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def text_split(value, sep='\n'):
    """Split text field"""
    return value.split(sep=sep)
