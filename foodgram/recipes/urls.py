from django.urls import path

from . import views


urlpatterns = [
    path('new/', views.RecipeCreate.as_view(), name='new_recipe'),
    path('shoplist/', views.ShopList.as_view(), name='shoplist'),
    path('shoplist/pdf/', views.ShopListPdf.as_view(), name='shoplistpdf'),
    path('shoplist/<int:pk>/delete/', views.ShopListDelete.as_view(),
         name='shoplist-delete'),
    path('recipe/<int:pk>/update/', views.RecipeUpdate.as_view(),
         name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.RecipeDelete.as_view(),
         name='recipe_delete'),
    path('', views.RecipeList.as_view(), name='index'),
    path('recipe/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
    path('<str:username>/<slug:slug>/',
         views.RecipeDetail.as_view(), name='recipe_slug'),
    path('favorites/',
         views.FavoriteRecipeList.as_view(), name='favorites'),
    path('subscriptions/',
         views.SubAuthorList.as_view(), name='subscription'),
    path('<str:username>/', views.AuthorRecipeList.as_view(), name='profile'),
]
