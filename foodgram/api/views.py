from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status
from rest_framework.response import Response


from recipes.models import Ingredient, Follow, Favorite, Recipe, ShoppingList
from .serializers import FavoriteSerializer, RecipeSerializer


User = get_user_model


class FavoriteView(views.APIView):
    permission_classes = [IsAuthenticated]
    request_model = Recipe
    operate_model = Favorite

    def post(self, request):
        user = self.request.user
        pk = request.data.get('id')
        if not (pk or pk.isdigit()):
            return Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            recipe = self.request_model.objects.get(pk=int(pk))
            instance = self.operate_model(user=user, recipe=recipe)
        except ObjectDoesNotExist:
            return Response({'success': 'false'}, status=status.HTTP_404_NOT_FOUND)
        instance.save()
        return Response({'success': 'true'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            recipe = self.request_model.objects.get(id=pk)
            instance = self.operate_model.objects.get(
                recipe=recipe, user=self.request.user)
        except ObjectDoesNotExist:
            return Response({'success': 'false'}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class ShoppingListView(FavoriteView):
    operate_model = ShoppingList


class FollowView(views.APIView):
    permission_classes = [IsAuthenticated]
    request_model = User
    arg_name = 'author'
    operate_model = ShoppingList

    def custom_create_obj(self, pk):
        kwargs['user'] = self.request.user
        kwargs[self.arg_name] = self.request_model.objects.get(pk=int(pk))
        return self.operate_model(**kwargs)

    def custom_get_obj(self, pk):
        kwargs['user'] = self.request.user
        kwargs[self.arg_name] = self.request_model.objects.get(pk=int(pk))
        return self.operate_model(**kwargs)

    def post(self, request):
        user = self.request.user
        pk = request.data.get('id')
        if not (pk or pk.isdigit()):
            return Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = self.create_obj(pk)
        except ObjectDoesNotExist:
            return Response({'success': 'false'}, status=status.HTTP_404_NOT_FOUND)
        instance.save()
        return Response({'success': 'true'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            recipe = self.request_model.objects.get(id=pk)
            instance = self.operate_model.objects.get(
                recipe=recipe, user=self.request.user)
        except ObjectDoesNotExist:
            return Response({'success': 'false'}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({'success': 'true'}, status=status.HTTP_200_OK)
