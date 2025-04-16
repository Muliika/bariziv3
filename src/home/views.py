from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from profiles.models import Profile, User

# Get CATEGORY_CHOICES from the User model
CATEGORY_CHOICES = User.CATEGORY_CHOICES


def home(request):
    return render(request, "index.html")


def sample_page(request):
    return render(request, "home/single-listing.html")


# def listings(request):
#     return render(request, "home/listings.html")


def categories(request):
    return render(request, "home/categories.html")


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


# def profiles_list(request):
#     """
#     View to display all business profiles
#     """
#     # Get only business profiles
#     profiles = Profile.objects.filter(user__user_type="business").select_related("user")

#     # Filter by business category if specified in query parameters
#     category = request.GET.get("category")
#     if category:
#         profiles = profiles.filter(user__business_category=category)


#     context = {
#         "profiles": profiles,
#         "category_choices": User.CATEGORY_CHOICES,
#     }
#     return render(request, "home/profiles_list.html", context)
def profiles_list(request):
    """
    View to display all business profiles with filtering options
    """
    # Get only business profiles
    profiles = Profile.objects.filter(user__user_type="business").select_related("user")

    # Initialize filter flags to track if any filters were applied
    filters_applied = False

    # Filter by keyword if specified
    keyword = request.GET.get("keyword", "")
    if keyword:
        filters_applied = True

        profiles = profiles.filter(
            Q(user__username__icontains=keyword)
            | Q(user__first_name__icontains=keyword)
            | Q(user__last_name__icontains=keyword)
            | Q(bio__icontains=keyword)
        )

    # Filter by business category if specified
    category = request.GET.get("category", "")
    if category and category != "All Categories":
        filters_applied = True
        profiles = profiles.filter(user__business_category=category)

    # Filter by location if specified
    location = request.GET.get("location", "")
    if location and location != "All Locations":
        filters_applied = True
        # Use district instead of city for location filtering
        profiles = profiles.filter(
            Q(district__icontains=location)
            | Q(county__icontains=location)
            | Q(parish__icontains=location)
        )

    # Sort results if specified
    sort_by = request.GET.get("sort", "newest")
    if sort_by == "newest":
        profiles = profiles.order_by("-user__date_joined")
    elif sort_by == "highest_rated":
        profiles = profiles.order_by("-rating")
    elif sort_by == "a_z":
        profiles = profiles.order_by("user__first_name", "user__last_name")

    # Get unique districts for location filter (instead of cities)
    districts = (
        Profile.objects.filter(user__user_type="business", district__isnull=False)
        .exclude(district="")
        .values_list("district", flat=True)
        .distinct()
    )

    # Convert to list and sort alphabetically
    locations_list = sorted(list(districts))

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(profiles, 6)  # Show 6 profiles per page

    try:
        paginated_profiles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_profiles = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_profiles = paginator.page(paginator.num_pages)

    # Count total results before pagination
    total_results = profiles.count()

    context = {
        "profiles": paginated_profiles,
        "category_choices": CATEGORY_CHOICES,  # Make sure this is imported or defined
        "cities": locations_list,  # We're using districts but keeping the variable name for template compatibility
        # Pass the current filter values back to the template
        "current_keyword": keyword,
        "current_category": category or "All Categories",
        "current_location": location or "All Locations",
        "current_sort": sort_by,
        "filters_applied": filters_applied,
        "total_results": total_results,
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
