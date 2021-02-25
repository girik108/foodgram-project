from django.urls import path

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteViewSet
 

router = DefaultRouter()
router.register('favorites', FavoriteView)
 
urlpatterns = [
    path('v1/', include(router.urls)),
]
 