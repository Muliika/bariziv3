# from django.urls import path

# from .views import add_post, index, listings, single_listing

# urlpatterns = [
#     path("", index, name="index"),
#     path("listings/", listings, name="listings"),
#     path("single-listing/", single_listing, name="single_listing"),
#     path("add-post/", add_post, name="add_post"),
# ]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="index"),
]
