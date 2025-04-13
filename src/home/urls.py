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

app_name = "home"

urlpatterns = [
    path("", views.home, name="index"),
    path("sample/", views.sample_page, name="sample_page"),
    path("listings/", views.listings, name="listings"),
    path("categories/", views.categories, name="categories"),
    path("businesses/", views.profiles_list, name="profiles_list"),
    path("business/<slug:slug>/", views.business_detail, name="business_detail"),
]
