from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm
from .models import Profile


# @login_required
def profile_view(request):
    """
    View to display the user's profile
    """
    # Try to get the profile, create it if it doesn't exist
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    context = {
        "profile": profile,
    }
    return render(request, "profiles/profile.html", context)


@login_required
def profile_edit(request):
    """
    View to edit the user's profile
    """
    # Try to get the profile, create it if it doesn't exist
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("/")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
    }
    return render(request, "profiles/profile-edit.html", context)


def bookmarks(request):
    """
    View to display the user's bookmarked listings
    """
    # For demonstration purposes, we'll create some sample bookmarks
    # In a real application, you would fetch this from your database
    sample_bookmarks = [
        {
            "id": 1,
            "title": "Modern Apartment in Downtown",
            "category": "For Rent",
            "price": "1,200",
            "location": "Downtown, New York",
            "bedrooms": 2,
            "bathrooms": 1,
            "area": 850,
            "image": "images/property-1.jpg",
        },
        {
            "id": 2,
            "title": "Luxury Villa with Pool",
            "category": "For Sale",
            "price": "450,000",
            "location": "Beverly Hills, Los Angeles",
            "bedrooms": 4,
            "bathrooms": 3,
            "area": 2200,
            "image": "images/property-2.jpg",
        },
        {
            "id": 3,
            "title": "Cozy Studio near University",
            "category": "For Rent",
            "price": "800",
            "location": "University District, Seattle",
            "bedrooms": 1,
            "bathrooms": 1,
            "area": 550,
            "image": "images/property-3.jpg",
        },
        {
            "id": 4,
            "title": "Family Home with Garden",
            "category": "For Sale",
            "price": "320,000",
            "location": "Suburbs, Chicago",
            "bedrooms": 3,
            "bathrooms": 2,
            "area": 1800,
            "image": "images/property-4.jpg",
        },
        {
            "id": 5,
            "title": "Penthouse with City View",
            "category": "For Rent",
            "price": "3,500",
            "location": "Financial District, San Francisco",
            "bedrooms": 3,
            "bathrooms": 2,
            "area": 1600,
            "image": "images/property-5.jpg",
        },
    ]

    context = {"bookmarks": sample_bookmarks}

    return render(request, "profiles/bookmarks.html", context)


def settings(request):
    """
    View to display the user's settings
    """
    return render(request, "profiles/settings.html")
