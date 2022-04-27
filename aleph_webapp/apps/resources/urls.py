from django.conf import settings
from django.urls import path
from .views import ResourceView
APP = getattr(settings, "APP", None)


urlpatterns = [path(r.url, ResourceView(r), name=r.__name__) for r in APP.RESOURCES]
