from rest_framework import serializers

from recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    dimension = serializers.StringRelatedField(read_only=True)

    class Meta:
        exclude = ('id',)
        model = Ingredient
