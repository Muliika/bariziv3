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
    path("businesses/", views.business_listing_list, name="business_listing_list"),
    path(
        "businesses/<slug:slug>/",
        views.business_listing_detail,
        name="business_listing_detail",
    ),
    path("businesses/<slug:slug>/claim/", views.claim_business, name="claim_business"),
    path("my-businesses/", views.my_businesses, name="my_businesses"),
    path(
        "claim-requests/<int:pk>/cancel/",
        views.cancel_claim_request,
        name="cancel_claim_request",
    ),
    path("business/<slug:slug>/edit/", views.edit_business, name="edit_business"),
    path("business/<slug:slug>/delete/", views.delete_business, name="delete_business"),
]
