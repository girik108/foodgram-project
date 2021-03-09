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

@register.filter(is_safe=True)
def widget_with_classes(value, arg):
    value.attrs['class'] += f' {arg}'
    return value  


@register.filter(is_safe=True)
def tag_with_classes(value, arg):
    value.attrs['class'] += f' {arg}'
    return value.tag  


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(is_safe=True)
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})


@register.filter
def is_auth(url, auth='/auth/'):
    return url.startswith(auth)


@register.filter
def is_index(url, index='/'):
    return url == index


@register.filter
def is_favorite(recipe, user):
    return recipe.is_favorite(user)


@register.filter
def is_purch(recipe, user):
    return recipe.is_purch(user)


@register.filter
def is_subscribe(user, author):
    return user.is_subscribe(author)
