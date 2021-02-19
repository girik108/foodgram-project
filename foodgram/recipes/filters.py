import django_filters

from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name='tag__slug')

    class Meta:
        model = Recipe
        fields = ['tag']
