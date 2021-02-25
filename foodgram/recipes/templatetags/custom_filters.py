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
<<<<<<< HEAD
def is_favorite(recipe, user):
    return recipe.is_favorite(user)
=======
def is_auth(url, auth='/auth/'): 
        return url.startswith(auth)


@register.filter 
def is_index(url, index='/'): 
        return url == index

>>>>>>> c28a9acc8cf7d803dbe8ec57047ad482706e4ca0
