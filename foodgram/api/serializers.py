from rest_framework import serializers

from recipes.models import Favorite, Recipe


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Favorite


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Recipe
        lookup_field='id'