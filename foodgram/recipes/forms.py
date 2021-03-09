from django import forms
from .models import Recipe, Tag, Ingredient


class TagSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'forms/widgets/checkbox.html'


    def id_for_label(self, id_, index=''):
        return id_
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        name = value.instance.slug
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['id'] = f'id_{value.instance.slug}'
            option['attrs']['class'] = f'tags__checkbox tags__checkbox_style_{value.instance.color}'
        return option
        


class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    tags = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Tag.objects.all(),
        widget=TagSelectMultiple(),
        label='Теги')

    ingredient = forms.ModelChoiceField(
        required=False, queryset=Ingredient.objects.all())

    class Meta:
        model = Recipe
        exclude = ('pk', 'author', 'slug', 'tags')
        labels = {'name': ('Название рецепта'),
                  'description': ('Описание'), 'image': ('Загрузить фото'),
                  'time': ('Время приготовления'), 'ingredient': 'Ингредиенты'}


    def clean_tags(self):
        tags = [slug for slug in Tag.objects.values_list('id', 'slug')]
        data = []

        for slug_id, slug in tags:
            if self.data.get(slug):
                data.append(slug_id)

        if not data:
            raise forms.ValidationError("TAGS empty")

        return data
