from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, mixins, viewsets, generics, status
from rest_framework.response import Response


from recipes.models import Ingredient, Follow, Favorite
from .serializers import FavoriteSerializer
# Create your views here.


class MixinAPIView(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    pass


class FavoriteView(MixinAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return user.favorites.all()
    
    #def get_object():
        pass

    #def perform_create(self, serializer):
        pass

    #def perform_destroy(self, instance):
        pass