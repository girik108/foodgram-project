import io
import os

from django.db.models import Sum

from django.http import FileResponse, HttpResponse, JsonResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from django.urls import reverse_lazy
from django.conf import settings

from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import View

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .models import Dimension, Recipe, Ingredient, RecipesIngredient, Tag, Follow, ShoppingList
from .forms import RecipeForm
from .filters import RecipeFilter


User = get_user_model()


class RecipeList(ListView):
    model = Recipe
    template_name = 'main/index.html'
    paginate_by = 6

    def get_queryset(self):
        qs = self.model.objects.all()
        recipe_filtered = RecipeFilter(self.request.GET, queryset=qs)
        return recipe_filtered.qs


class AuthorRecipeList(ListView):
    model = Recipe
    template_name = 'author/index.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        qs = self.author.recipes.all()
        recipe_filtered = RecipeFilter(self.request.GET, queryset=qs)
        return recipe_filtered.qs


class FavoriteRecipeList(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'favorite/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite'] = True
        return context

    def get_queryset(self):
        return Recipe.objects.filter(liked__user=self.request.user)


class SubAuthorList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'follow/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subs'] = True
        return context

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=self.request.user)


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'detail/index.html'

    def get_context_data(self, **kwargs):
        recipe = self.get_object()
        context = super().get_context_data(**kwargs)
        context['ingredients'] = recipe.ingredients.all()
        context['single'] = True
        return context


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'create/create.html'
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        VALUES = {'name': 'nameIngredient',
                  'value': 'valueIngredient',
                  'units': 'unitsIngredient', }
        form = self.form_class(request.POST)
        if form.is_valid():
            keys = request.POST.keys()
            result = {}
            keys = [key for key in keys if key.startswith(VALUES['name'])]
            for key in keys:
                name, num = key.split('_')
                dct = {}
                dct[name] = request.POST[key]
                dct[VALUES[1]] = request.POST[VALUES[1] + '_' + num]
                result[num] = dct

            return JsonResponse(result)

        return JsonResponse(form.errors)


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


class ShopList(LoginRequiredMixin, ListView):
    model = ShoppingList
    template_name = 'shoplist/index.html'
    paginate_by = 10
    context_object_name = 'shoplists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoplist'] = True
        return context

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)


class ShopListDelete(LoginRequiredMixin, DeleteView):
    model = ShoppingList
    success_url = reverse_lazy('shoplist')
    template_name = 'shoplist/confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(ShopListDelete, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj


class ShopListPdf(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        #ingr = RecipesIngredient.objects.filter(recipe__purchased__user=self.request.user).values('ingredient').annotate(summ=Sum('count'))
        #ingr = Ingredient.objects.filter()
        
        STATIC_DIR = settings.STATIC_ROOT
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('LiberationSerif', os.path.join(
            STATIC_DIR, 'fonts/liberation-serif.ttf'), 'UTF-8'))
        p.setFont('LiberationSerif', 20)
        p.setLineWidth(.3)
        p.drawCentredString(300, 750, 'Список покупок')
        p.line(50, 740, 550, 740)
        step = 30
        for num, item in enumerate(ingr):
            p.drawString(50, 720-num*step, f'{item}')
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='shoplist.pdf')
