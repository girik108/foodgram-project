from django import forms
from .models import Recipe, Tag, Ingredient


class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(), label='Теги')

    ingredient = forms.ModelChoiceField(
        required=False, queryset=Ingredient.objects.all())

    class Meta:
        model = Recipe
        exclude = ('pk', 'author', 'slug')
        labels = {'name': ('Название рецепта'),
                  'description': ('Описание'), 'image': ('Загрузить фото'),
                  'time': ('Время приготовления'), 'ingredient': 'Ингредиенты'}
