from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .filters import RecipeFilter
from .forms import RecipeForm
from .models import Ingredient, Recipe, ShoppingList
from .permissions import LoginPermissionMixin, ShopListPermission
from .utils import create_pdf


PAGINATE = 6
User = get_user_model()


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
        context['author_index'] = True
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
        recipe = form.custom_save(author=request.user)
        if recipe:
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
        recipe = form.custom_save(author=request.user, update=True)

        if recipe:
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
            kwargs['ingredients__recipe__purchased__user'] = self.request.user
        else:
            sess_key = self.request.session.session_key
            kwargs['ingredients__recipe__purchased__session_key'] = sess_key

        ingredients = Ingredient.objects.filter(
            **kwargs).annotate(summ=Sum('ingredients__count'))

        buffer = create_pdf(ingredients)

        return FileResponse(buffer, as_attachment=True,
                            filename='shoplist.pdf')
