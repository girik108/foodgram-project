from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page


from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from .models import Unit, Recipe, Ingredient, RecipesIngredient, Tag
#from .forms import PostForm, CommentForm


User = get_user_model()

class RecipeList(ListView):
    model = Recipe
    template_name = 'index.html'


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        recipe = self.get_object()
        context = super().get_context_data(**kwargs)
        #ingredients = Ingredient.objects.filter(recipes__recipe=recipe)
        ingredients = recipe.ingredients.all()
        context['ingredients'] = ingredients
        return context
    
def index(request):
    user = User.objects.get(id=1)
    ingredients = RecipesIngredient.objects.filter(recipe__author=user)
    result = list(ingredients)
    
    return HttpResponse(f'{result}')

    #return render(request, 'index.html', {'page': page, 'paginator': paginator})