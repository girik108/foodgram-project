from django.contrib import admin

from recipes import models

class DimensionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'abbr')
    search_fields = ('title', 'abbr')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description',
                    'pub_date', 'image', 'author', 'time')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipesIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'count',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')

class ShoppingListAdmin(admin.ModelAdmin): 
    list_display = ('pk', 'user', 'recipe')

admin.site.register(models.Dimension, DimensionAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.RecipesIngredient, RecipesIngredientAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Follow, FollowAdmin)
admin.site.register(models.Favorite, FavoriteAdmin)
admin.site.register(models.ShoppingList, ShoppingListAdmin)