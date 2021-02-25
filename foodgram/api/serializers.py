from rest_framework import serializers

from recipes.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Favorite
