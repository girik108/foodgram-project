from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy


from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse

from .models import Unit, Recipe, Ingredient, RecipesIngredient, Tag
from .forms import RecipeForm


User = get_user_model()


class RecipeList(ListView):
    model = Recipe
    template_name = 'index_auth.html'
    paginate_by = 10


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        recipe = self.get_object()
        context = super().get_context_data(**kwargs)
        #ingredients = Ingredient.objects.filter(recipes__recipe=recipe)
        ingredients = recipe.ingredients.all()
        context['ingredients'] = ingredients
        context['single'] = True
        return context


class RecipeCreate(CreateView):
    model = Recipe
    template_name = 'add.html'
    form_class = RecipeForm
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tags'] = Tag.objects.all()
        return context

class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['name']

class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes')