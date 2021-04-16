from django import forms
from django.shortcuts import get_object_or_404

from .models import Ingredient, Recipe, RecipesIngredient, Tag


class RecipeForm(forms.ModelForm):

    tags = forms.MultipleChoiceField(
        required=False,
        label='Теги')

    ingredient = forms.MultipleChoiceField(
        required=False,
        label='Ингредиенты')

    class Meta:
        model = Recipe
        exclude = ('pk', 'author', 'tags')
        labels = {'image': ('Загрузить фото'), }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    def custom_save(self, author, update=False):
        if self.is_valid():
            recipe = self.save(commit=False)
            if not update:
                recipe.author = author
                recipe.save()
            else:
                recipe.save()
                recipe.tags.clear()

                ingredients = [ingr.id for ingr,
                               count in self.cleaned_data['ingredient']]
                recipe.ingredients.exclude(
                    ingredient__in=ingredients).delete()

            recipe.tags.add(*self.cleaned_data['tags'])
            for ingr, count in self.cleaned_data['ingredient']:
                RecipesIngredient.objects.update_or_create(
                    ingredient=ingr, recipe=recipe, count=count)

            return recipe

        return None

    def clean_tags(self):
        tags_all = Tag.objects.all()
        tag_slugs = tags_all.values_list('slug', flat=True)
        slugs = [slug for slug in tag_slugs if self.data.get(slug)]
        data = tags_all.filter(slug__in=slugs)
        if not data:
            raise forms.ValidationError('Необходимо отметить хотя бы один тег')

        return data

    def clean_ingredient(self):
        VALUES = {'name': 'nameIngredient',
                  'value': 'valueIngredient',
                  'units': 'unitsIngredient', }

        data = []
        keys = self.data.keys()
        keys = [key for key in keys if key.startswith(VALUES['name'])]
        for key in keys:
            name, num = key.split('_')
            title = self.data.get(key)

            ingredient = get_object_or_404(Ingredient, title=title.lower())
            if not ingredient:
                continue
            if num:
                count = self.data.get('_'.join((VALUES['value'], num)))
            else:
                count = self.data.get(VALUES['value'])

            if not count.isdecimal() or int(count) < 0:
                raise forms.ValidationError(
                    'Количество должно быть положительным числом')

            data.append((ingredient, int(count)))

        if not data:
            raise forms.ValidationError('Добавьте ингредиенты')

        return data
