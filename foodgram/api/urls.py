from django.urls import path, include

from .views import FavoriteView, ShoppingListView, FollowView, IngredientView


api_urls = [
    path('favorites/', FavoriteView.as_view(),
         name='favorite_add'),
    path('favorites/<int:pk>/', FavoriteView.as_view(),
         name='favorite_del'),
    path('purchases/', ShoppingListView.as_view(),
         name='purchase_add'),
    path('purchases/<int:pk>/', ShoppingListView.as_view(),
         name='purchase_del'),
    path('subscriptions/', FollowView.as_view(),
         name='subscription_add'),
    path('subscriptions/<int:pk>/', FollowView.as_view(),
         name='subscription_del'),
    path('ingredients/', IngredientView.as_view(),
         name='ingredients'),
]

urlpatterns = [
    path('v1/', include(api_urls)),
]
