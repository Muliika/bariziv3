from allauth.account.views import LoginView, LogoutView, SignupView
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    # Profile view and edit
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    # Bookmarks
    path("bookmarks/", views.bookmarks, name="bookmarks"),
    # Authentication URLs (redirects to allauth views)
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # Password management
    path(
        "password/change/",
        RedirectView.as_view(pattern_name="account_change_password"),
        name="password_change",
    ),
    path(
        "password/reset/",
        RedirectView.as_view(pattern_name="account_reset_password"),
        name="password_reset",
    ),
]
