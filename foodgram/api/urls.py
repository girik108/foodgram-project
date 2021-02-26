from django.urls import path

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteView, ShoppingListView
 
 
urlpatterns = [
    path('v1/favorites/', FavoriteView.as_view()),
    path('v1/favorites/<int:pk>/', FavoriteView.as_view()),
    path('v1/purchases/', ShoppingListView.as_view()),
    path('v1/purchases/<int:pk>/', ShoppingListView.as_view()),
    path('v1/subscriptions/', ShoppingListView.as_view()),
    path('v1/subscriptions/<int:pk>/', ShoppingListView.as_view()),
]