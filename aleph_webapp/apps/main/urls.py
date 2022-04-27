from django.urls import path
from . import views

# --------------------------------------------------------------------------------------------------------------
# Urls
# --------------------------------------------------------------------------------------------------------------
urlpatterns = [
    path('', views.Home, name='index'),
    path('home', views.Home, name='home'),
    path('login', views.Login, name='login'),
    path('logout', views.Logout, name='logout'),
    path('password_change', views.ChangePassword, name='password_change'),
]
