from django.db.models import Sum

from django.http import FileResponse, HttpResponse, JsonResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from django.urls import reverse_lazy
from django.conf import settings

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import View


from .models import Dimension, Recipe, Ingredient, RecipesIngredient, Tag, Follow, ShoppingList
from .forms import RecipeForm
from .filters import RecipeFilter
from .utils import create_pdf
from .permissions import LoginPermissionMixin, ShopListPermission


PAGINATE = 6
User = get_user_model()

@method_decorator(cache_page(60 * 5), name='dispatch')
class RecipeList(ListView):
    model = Recipe
    paginate_by = PAGINATE

    def get_queryset(self):
        qs = self.model.objects.all().prefetch_related(
            'tags', 'author', 'purchased__user', 'liked__user')
        recipe_filtered = RecipeFilter(self.request.GET, queryset=qs)
        return recipe_filtered.qs


class AuthorRecipeList(ListView):
    model = Recipe
    template_name = 'recipes/author_recipe_list.html'
    paginate_by = PAGINATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        qs = self.author.recipes.all().prefetch_related(
            'tags')
        recipe_filtered = RecipeFilter(self.request.GET, queryset=qs)
        return recipe_filtered.qs


class FavoriteRecipeList(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'favorite/index.html'
    paginate_by = PAGINATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite'] = True
        return context

    def get_queryset(self):
        qs = self.model.objects.filter(
            liked__user=self.request.user).prefetch_related('tags', 'author')
        recipe_filtered = RecipeFilter(self.request.GET, queryset=qs)
        return recipe_filtered.qs


class SubAuthorList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'follow/index.html'
    paginate_by = PAGINATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subs'] = True
        return context

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=self.request.user)


class RecipeDetail(DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        recipe = self.get_object()
        context = super().get_context_data(**kwargs)
        context['ingredients'] = recipe.ingredients.all().select_related(
            'ingredient')
        context['detail'] = True
        return context


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, files=request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe.tags.add(*form.cleaned_data['tags'])

            for ingr, count in form.cleaned_data['ingredient']:
                RecipesIngredient.objects.create(
                    ingredient=ingr, recipe=recipe, count=count)

            return redirect('recipe', recipe.id)

        return render(request, self.template_name, {'form': form})


class RecipeUpdate(LoginPermissionMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        recipe = self.get_object()
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        context['recipe_tags'] = list(
            recipe.tags.values_list('slug', flat=True))
        ing_lst = recipe.ingredients.all().prefetch_related('ingredient')
        context['recipe_ingredients'] = enumerate(ing_lst, start=1)
        return context

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        form = self.form_class(request.POST or None,
                               files=request.FILES or None, instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            recipe.tags.clear()
            recipe.tags.add(*form.cleaned_data['tags'])

            ingredients = [ingr.id for ingr,
                           count in form.cleaned_data['ingredient']]

            recipe.ingredients.exclude(ingredient__in=ingredients).delete()

            for ingr, count in form.cleaned_data['ingredient']:
                RecipesIngredient.objects.update_or_create(
                    ingredient=ingr, recipe=recipe, count=count)

            return redirect('recipe', recipe.id)

        return render(request, self.template_name, {'form': form})


class RecipeDelete(LoginPermissionMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('index')


class ShopList(ListView):
    model = ShoppingList
    template_name = 'shoplist/index.html'
    context_object_name = 'shoplists'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shoplist'] = True
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.purchases.all()
        session_key = self.request.session.session_key
        return self.model.objects.filter(session_key=session_key)


class ShopListDelete(ShopListPermission, DeleteView):
    model = ShoppingList
    success_url = reverse_lazy('shoplist')
    template_name = 'shoplist/confirm_delete.html'


class ShopListPdf(View):
    def get(self, request, *args, **kwargs):
        kwargs = {}
        if request.user.is_authenticated:
            kwargs['recipes__recipe__purchased__user'] = self.request.user
        else:
            kwargs['recipes__recipe__purchased__session_key'] = self.request.session.session_key

        ingredients = Ingredient.objects.filter(
            **kwargs).annotate(summ=Sum('recipes__count'))

        buffer = create_pdf(ingredients)

        return FileResponse(buffer, as_attachment=True, filename='shoplist.pdf')


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.build_absolute_uri()}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'misc/403.html', {'path': request.build_absolute_uri()}, status=403)
