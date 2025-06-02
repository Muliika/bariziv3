from django.urls import path

from . import views

app_name = "attractions"

urlpatterns = [
    path("", views.AttractionListView.as_view(), name="attraction_list"),
    path(
        "<slug:city_slug>/<slug:slug>/",
        views.AttractionDetailView.as_view(),
        name="attraction_detail",
    ),
]
