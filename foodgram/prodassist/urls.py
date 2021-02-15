from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('recipes/', views.RecipeList.as_view(), name='recipes'),
    path('recipes/<slug:slug>/', views.RecipeDetail.as_view(), name='recipe'),
]