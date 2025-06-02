from django.urls import path

from . import views

app_name = "cities"

urlpatterns = [
    # Class-based view URLs
    path("districts/", views.DistrictListView.as_view(), name="district_list"),
    path(
        "districts/<slug:slug>/",
        views.DistrictDetailView.as_view(),
        name="district_detail",
    ),
    path("cities/", views.CityListView.as_view(), name="city_list"),
    path("cities/<slug:slug>/", views.CityDetailView.as_view(), name="city_detail"),
    path(
        "cities/<slug:city_slug>/attractions/<slug:slug>/",
        views.AttractionDetailView.as_view(),
        name="attraction_detail",
    ),
]
