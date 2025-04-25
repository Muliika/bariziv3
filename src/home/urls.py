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
    path("listings/", views.profiles_list, name="listings"),
    path("categories/", views.categories, name="categories"),
    path("businesses/", views.profiles_list, name="profiles_list"),
    path("business/<slug:slug>/", views.business_detail, name="business_detail"),
    path("contact/", views.contact_view, name="contact"),
    path("about/", views.about, name="about"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path("about-uganda/", views.about_uganda, name="about_uganda"),
]
