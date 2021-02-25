from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, mixins, viewsets
from rest_framework import generics

from recipes.models import Ingredient, Follow, Favorite
from .serializers import FavoriteSerializer
# Create your views here.


class MixinAPIView(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    pass


class FavoriteView(MixinAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
