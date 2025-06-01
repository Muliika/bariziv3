from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from profiles.models import Profile, User

# Get CATEGORY_CHOICES from the User model
CATEGORY_CHOICES = User.CATEGORY_CHOICES


# def home(request):
#     return render(request, "index.html")


def home(request):
    # Get all categories from CATEGORY_CHOICES
    categories = [
        {
            "name": category[1],  # Display name
            "value": category[0],  # Value stored in database
            "icon": get_category_icon(
                category[0]
            ),  # Get appropriate icon for each category
            "count": Profile.objects.filter(
                user__business_category=category[0], user__user_type="business"
            ).count(),  # Count of businesses in this category
        }
        for category in CATEGORY_CHOICES
    ]

    # Get featured business profiles
    # Featured profiles are those with featured=True flag
    featured_profiles = (
        Profile.objects.filter(user__user_type="business", featured=True)
        .select_related("user")
        .order_by("-rating")[:6]
    )  # Limit to 6 featured listings

    # Get latest business profiles
    # These are the most recently added business profiles
    latest_profiles = (
        Profile.objects.filter(user__user_type="business")
        .select_related("user")
        .order_by("-user__date_joined")[
            :6
        ]  # Limit to 6 latest listings, ordered by join date
    )

    context = {
        "categories": categories,
        "featured_profiles": featured_profiles,
        "latest_profiles": latest_profiles,
    }
    return render(request, "index.html", context)


# Helper function to map category values to Bootstrap icons
def get_category_icon(category_value):
    icon_mapping = {
        "accommodation": "house-door",
        "food_drinks": "cup-hot",
        "shopping": "shop",
        "activities": "bicycle",
        "health": "heart-pulse",
        "travel": "car-front",
        "entertainment": "music-note-beamed",
        "attractions": "bank",
        "services": "tools",
        "education": "book",
        "other": "three-dots",
    }
    # Return the mapped icon or a default one if not found
    return icon_mapping.get(category_value, "tag")


def sample_page(request):
    return render(request, "home/single-listing.html")


def categories(request):
    # Get all categories from CATEGORY_CHOICES
    categories = [
        {
            "name": category[1],  # Display name
            "value": category[0],  # Value stored in database
            "icon": get_category_icon(
                category[0]
            ),  # Get appropriate icon for each category
            "count": Profile.objects.filter(
                user__business_category=category[0], user__user_type="business"
            ).count(),  # Count of businesses in this category
        }
        for category in CATEGORY_CHOICES
    ]

    context = {"categories": categories}
    return render(request, "home/categories.html", context)


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")

        # Construct email message
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # Send email
            send_mail(
                f"Contact Form: {subject}",
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # You'll need to define this in settings
                fail_silently=False,
            )
            messages.success(
                request,
                "Your message has been sent successfully. We'll get back to you soon!",
            )
            return redirect("home:contact")
        except Exception as e:
            messages.error(
                request,
                f"There was an error sending your message. Please try again later.",
            )

    return render(request, "home/contact-form.html")


def profiles_list(request):
    """
    View to display and filter business profiles
    """
    # Get all profiles that are businesses
    profiles = Profile.objects.filter(user__user_type="business").select_related("user")

    # Get filter parameters from request
    keyword = request.GET.get("keyword", "")
    category = request.GET.get("category", "All Categories")
    location = request.GET.get("location", "All Locations")
    sort = request.GET.get("sort", "newest")

    # Apply filters
    filters_applied = False

    # Keyword search (search in name, bio, and description)
    if keyword:
        filters_applied = True
        profiles = profiles.filter(
            Q(user__first_name__icontains=keyword)
            | Q(user__last_name__icontains=keyword)
            | Q(bio__icontains=keyword)
            | Q(description__icontains=keyword)  # Changed from services to description
        )

    # Category filter
    if category and category != "All Categories":
        filters_applied = True
        profiles = profiles.filter(user__business_category=category)

    # Location filter
    if location and location != "All Locations":
        filters_applied = True
        profiles = profiles.filter(
            Q(district__icontains=location)
            | Q(county__icontains=location)
            | Q(parish__icontains=location)
        )

    # Apply sorting
    if sort == "newest":
        profiles = profiles.order_by("-user__date_joined")
    elif sort == "highest_rated":
        profiles = profiles.order_by("-rating")
    elif sort == "a_z":
        profiles = profiles.order_by("user__first_name")

    # Get all unique cities/districts for location filter
    cities = (
        Profile.objects.filter(user__user_type="business")
        .exclude(district__isnull=True)
        .exclude(district__exact="")
        .values_list("district", flat=True)
        .distinct()
    )

    # Pagination
    paginator = Paginator(profiles, 9)  # Show 9 profiles per page
    page = request.GET.get("page")
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    # Get all category choices for the filter dropdown
    category_choices = CATEGORY_CHOICES

    context = {
        "profiles": profiles,
        "total_results": paginator.count,
        "category_choices": category_choices,
        "cities": cities,
        "current_keyword": keyword,
        "current_category": category,
        "current_location": location,
        "current_sort": sort,
        "filters_applied": filters_applied,
    }

    return render(request, "home/listings.html", context)


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


def about(request):
    """
    View to display the about us page
    """
    # You can add any context data needed for the about page here
    context = {
        "page_title": "About Us",
        "team_members": [
            {
                "name": "Sarah Johnson",
                "position": "Founder & CEO",
                "image": "images/team-1.jpg",
                "linkedin": "#",
                "twitter": "#",
                "email": "#",
            },
            {
                "name": "Michael Chen",
                "position": "CTO",
                "image": "images/team-2.jpg",
                "linkedin": "#",
                "twitter": "#",
                "email": "#",
            },
            {
                "name": "Olivia Rodriguez",
                "position": "Head of Marketing",
                "image": "images/team-3.jpg",
                "linkedin": "#",
                "twitter": "#",
                "email": "#",
            },
        ],
        "stats": {
            "businesses": "10,000+",
            "users": "500,000+",
            "cities": "50+",
            "satisfaction": "100%",
        },
        "timeline": [
            {
                "year": "2018",
                "title": "The Beginning",
                "description": "Barizi was founded with a simple idea: to create a better way for people to discover local businesses.",
            },
            {
                "year": "2019",
                "title": "First 1,000 Users",
                "description": "We celebrated our first milestone of 1,000 active users and 100 registered businesses.",
            },
            {
                "year": "2020",
                "title": "Expansion",
                "description": "Despite global challenges, we expanded to 10 new cities and launched our mobile app.",
            },
            {
                "year": "2021",
                "title": "Series A Funding",
                "description": "Secured our first major investment round, allowing us to grow our team and improve our platform.",
            },
            {
                "year": "2022",
                "title": "Going International",
                "description": "Expanded beyond our home country to bring Barizi to international markets.",
            },
            {
                "year": "2023",
                "title": "Today",
                "description": "Continuing to innovate and grow, with a focus on enhancing user experience and supporting local businesses.",
            },
        ],
        "testimonials": [
            {
                "text": "Barizi has completely transformed how I find local services. The platform is intuitive, and I've discovered so many amazing businesses I wouldn't have found otherwise.",
                "name": "David Wilson",
                "position": "Regular User",
                "image": "images/testimonial-1.jpg",
            },
            {
                "text": "As a small business owner, joining Barizi was one of the best decisions I've made. My customer base has grown significantly, and the platform makes it easy to showcase what makes my business special.",
                "name": "Maria Garcia",
                "position": "Business Owner",
                "image": "images/testimonial-2.jpg",
            },
            {
                "text": "The Barizi team truly cares about both users and businesses. Their customer support is exceptional, and they're always innovating to make the platform better.",
                "name": "James Thompson",
                "position": "Premium Member",
                "image": "images/testimonial-3.jpg",
            },
        ],
    }
    return render(request, "home/about.html", context)


def terms_of_service(request):
    """
    View to display the terms of service page
    """
    return render(request, "home/terms.html")


def privacy_policy(request):
    """
    View to display the privacy policy page
    """
    return render(request, "home/privacy.html")


def disclaimer(request):
    """
    View to display the disclaimer page
    """
    return render(request, "home/disclaimer.html")


def about_uganda(request):
    """
    View to display the about uganda page
    """
    return render(request, "home/about_uganda.html")
