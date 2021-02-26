from django.contrib import admin

from .models import Unit, Recipe, Ingredient, RecipesIngredient, Tag, Follow, Favorite, ShoppingList


class UnitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'abbr')
    search_fields = ('name', 'abbr')
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


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')

class ShoppingListAdmin(admin.ModelAdmin): 
    list_display = ('pk', 'user', 'recipe')

admin.site.register(Unit, UnitAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipesIngredient, RecipesIngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)