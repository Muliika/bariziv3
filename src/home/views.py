from django.shortcuts import get_object_or_404, render

from profiles.models import Profile, User


def home(request):
    return render(request, "index.html")


def sample_page(request):
    return render(request, "home/single-listing.html")


def listings(request):
    return render(request, "home/listings.html")


def categories(request):
    return render(request, "home/categories.html")


def profiles_list(request):
    """
    View to display all business profiles
    """
    # Get only business profiles
    profiles = Profile.objects.filter(user__user_type="business").select_related("user")

    # Filter by business category if specified in query parameters
    category = request.GET.get("category")
    if category:
        profiles = profiles.filter(user__business_category=category)

    context = {
        "profiles": profiles,
        "category_choices": User.CATEGORY_CHOICES,
    }
    return render(request, "home/profiles_list.html", context)


def business_detail(request, slug):
    """
    View to display detailed information about a business profile
    """
    # Get the user by slug and ensure it's a business
    user = get_object_or_404(User, slug=slug, user_type="business")
    profile = get_object_or_404(Profile, user=user)

    context = {
        "profile": profile,
        "user": user,
    }
    return render(request, "home/business_detail.html", context)
