from django.urls import path

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteView
 


router = DefaultRouter()
router.register('favorites', FavoriteView)


urlpatterns = [
    path('v1/', include(router.urls)),
]
 
#urlpatterns = [
#    path('v1/favorites/', FavoriteView.as_view()),
#    path('v1/favorites/<int:pk>/', FavoriteView.as_view())
#]