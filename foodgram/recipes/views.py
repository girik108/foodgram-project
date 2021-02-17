from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.urls import reverse_lazy

from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import View


from django.http import HttpResponse

from .models import Unit, Recipe, Ingredient, RecipesIngredient, Tag, Follow
from .forms import RecipeForm


User = get_user_model()


class RecipeList(ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 10


class FavoriteRecipeList(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite'] = True
        return context

    def get_queryset(self):
        return Recipe.objects.filter(liked__user=self.request.user)


class SubRecipeList(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subs'] = True
        return context

    def get_queryset(self):
        return Recipe.objects.filter(author__following__user=self.request.user)


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        recipe = self.get_object()
        context = super().get_context_data(**kwargs)
        context['ingredients'] = recipe.ingredients.all()
        context['single'] = True
        return context


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'add.html'
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tags'] = Tag.objects.all()
        return context


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['name']


class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes')


class FollowUser(LoginRequiredMixin, View):
    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        if author != request.user:
            follow, created = Follow.objects.get_or_create(
                user=request.user, author=author)
        return redirect('recipe', author, 1)


class UnFollowUser(LoginRequiredMixin, View):
    pass
