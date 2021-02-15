from django.contrib import admin

from .models import Unit, Recipe, Ingredient, RecipesIngredient, Tag


class UnitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'text',
                    'pub_date', 'image', 'author', 'time')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipesIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient',
                    'unit', 'count',)


admin.site.register(Unit, UnitAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipesIngredient, RecipesIngredientAdmin)
admin.site.register(Tag, TagAdmin)
