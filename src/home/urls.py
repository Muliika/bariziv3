from django.urls import path

from .views import index, listings

urlpatterns = [
    path("", index, name="index"),
    path("listings/", listings, name="listings"),
]
