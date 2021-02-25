from django import template
from django.template.defaultfilters import stringfilter

from recipes.models import Favorite


register = template.Library()


@register.filter
@stringfilter
def text_split(value, sep='\n'):
    """Split text field"""
    return value.split(sep=sep)


@register.filter 
def addclass(field, css): 
        return field.as_widget(attrs={"class": css})


@register.filter 
def is_favorite(recipe, user):
    return recipe.is_favorite(user)
