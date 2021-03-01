from django import forms
from .models import Recipe, Tag, Ingredient


class RecipeForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple,)
    
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all())

    class Meta:
        model = Recipe
        exclude = ('pk','author')
