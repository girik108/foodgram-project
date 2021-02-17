from django.urls import path

from . import views


# recipes urls
urlpatterns = [
    path('new/', views.RecipeCreate.as_view(), name='new_recipe'),
    path('<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe-update'),
    path('<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe-delete'),
    path('', views.RecipeList.as_view(), name='index'),
    path('<str:username>/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
    path('<str:username>/favorites/',
         views.FavoriteRecipeList.as_view(), name='favorites'),
    path('<str:username>/subscriptions/',
         views.SubRecipeList.as_view(), name='subscription'),
    path('<str:username>/<slug:slug>/',
         views.RecipeDetail.as_view(), name='recipe_slug'),
]
# favorites url

urlpatterns += [
    path('<str:username>/follow/', views.FollowUser, name='user_follow'),
    path('<str:username>/unfollow/', views.UnFollowUser, name='user_unfollow'),
]

# shoping list urls
