from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import views, status
from rest_framework.response import Response

from recipes.models import Ingredient, Follow, Favorite, Recipe, ShoppingList
from .serializers import IngredientSerializer
from .utils import FollowError, FavoriteError


User = get_user_model()


class IngredientView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('query')
        serializer = IngredientSerializer(
            Ingredient.objects.filter(title__startswith=query), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FavoriteView(views.APIView):
    permission_classes = [IsAuthenticated]
    request_model = Recipe
    operate_model = Favorite
    arg_name = 'recipe'

    def get_kwargs(self, pk):
        kwargs = {}
        kwargs['user'] = self.request.user
        kwargs[self.arg_name] = self.request_model.objects.get(pk=int(pk))

        return kwargs

    def custom_create_obj(self, pk):
        kwargs = self.get_kwargs(pk)
        if kwargs[self.arg_name].author == kwargs['user']:
            raise FavoriteError

        return self.operate_model(**kwargs)

    def custom_get_obj(self, pk):
        kwargs = self.get_kwargs(pk)
        return self.operate_model.objects.get(**kwargs)

    def post(self, request):
        pk = request.data.get('id')
        if not (pk or pk.isdigit()):
            return Response({'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.custom_create_obj(pk)
        instance.save()

        return Response({'success': 'true'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        instance = self.custom_get_obj(pk)
        instance.delete()

        return Response({'success': 'true'}, status=status.HTTP_200_OK)


class FollowView(FavoriteView):
    permission_classes = [IsAuthenticated]
    request_model = User
    arg_name = 'author'
    operate_model = Follow

    def custom_create_obj(self, pk):
        kwargs = self.get_kwargs(pk)
        if kwargs['user'] == kwargs[self.arg_name]:
            raise FollowError

        return self.operate_model(**kwargs)


class ShoppingListView(FavoriteView):
    operate_model = ShoppingList
    permission_classes = [AllowAny]

    def get_kwargs(self, pk):
        kwargs = super().get_kwargs(pk)
        kwargs['user'] = kwargs['user'] if kwargs['user'].is_authenticated else None
        if not self.request.session.session_key:
            self.request.session.save()
        kwargs['session_key'] = self.request.session.session_key

        return kwargs

    def custom_create_obj(self, pk):
        kwargs = self.get_kwargs(pk)

        return self.operate_model(**kwargs)
