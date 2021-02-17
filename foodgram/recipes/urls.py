from django.urls import path

from . import views


# recipes urls
urlpatterns = [
    path('new/', views.RecipeCreate.as_view(), name='recipe-add'),
    path('<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe-update'),
    path('<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe-delete'),
    path('', views.RecipeList.as_view(), name='recipes'),
    path('<str:username>/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
    path('<str:username>/<slug:slug>/', views.RecipeDetail.as_view(), name='recipe_slug'),
]
#favorites url

#shoping list urls