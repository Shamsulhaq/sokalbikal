from django.urls import path

from .views import (
    UserLoginView,
    UserRegistrationView,
    get_logout, HomeView,ProfileView
)

urlpatterns = [
    path('index/', HomeView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', get_logout, name='logout')
]
