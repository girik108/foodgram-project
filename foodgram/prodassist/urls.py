from django.urls import path

from . import views


# recipes urls
urlpatterns = [
    path('add/', views.RecipeCreate.as_view(), name='recipe-add'),
    path('<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe-update'),
    path('<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe-delete'),
    path('', views.RecipeList.as_view(), name='recipes'),
    path('<int:pk>/', views.RecipeDetail.as_view(), name='detail-recipe-pk'),
    path('<slug:slug>/', views.RecipeDetail.as_view(), name='detail-recipe-slug'),
]
#favorites url

#shoping list urls