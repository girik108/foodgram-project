from django import forms
from .models import Recipe, Tag, Ingredient


class TagSelectMultiple(forms.CheckboxSelectMultiple):
    #template_name = 'forms/widgets/checkbox.html'


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

    tags = forms.MultipleChoiceField(
        required=False,
        label='Теги')

    ingredient = forms.MultipleChoiceField(
        required=False,
        widget=forms.HiddenInput(),
        label='Ингредиенты')

    class Meta:
        model = Recipe
        exclude = ('pk', 'author', 'slug', 'tags')
        labels = {'name': ('Название рецепта'),
                  'description': ('Описание'), 'image': ('Загрузить фото'),
                  'time': ('Время приготовления')}


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

            ingredient = Ingredient.objects.get(title=title.lower())
            if not ingredient:
                continue
            
            if num:
                count = self.data.get('_'.join((VALUES['value'], num)))
            else:
                count = self.data.get(VALUES['value'])
            
            data.append((ingredient, int(count)))

        if not data:
            raise forms.ValidationError('Добавьте ингредиенты')

        return data