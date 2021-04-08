from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(),
         name='signup'),
    path('password_change/', views.PassChange.as_view(),
         name='password_change'),
    path('password_reset/', views.PassReset.as_view(),
         name='password_reset'),
    path('login/', views.UserLoginView.as_view(),
         name='login'),
]
