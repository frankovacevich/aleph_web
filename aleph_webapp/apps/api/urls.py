from django.urls import path
from . import views


# --------------------------------------------------------------------------------------------------------------
# Urls
# --------------------------------------------------------------------------------------------------------------
urlpatterns = [
    path('', views.ApiKeys, name='api_keys'),
    path('<str:key>', views.ApiData, name='api_data'),
]
