# from django.shortcuts import render


# def index(request):
#     return render(request, "index.html")


# def listings(request):
#     return render(request, "home/listings.html")


# def single_listing(request):
#     return render(request, "home/single-listing.html")


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden

# def add_post(request):
#     return render(request, "home/add-post.html")
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BusinessListingForm, ClaimRequestForm
from .models import BusinessListing, ClaimRequest


def home(request):
    """
    Home page view
    """
    # Get featured listings for the homepage
    featured_listings = BusinessListing.objects.filter(featured=True)[:6]

    context = {
        "featured_listings": featured_listings,
    }

    return render(request, "index.html", context)


def business_listing_list(request):
    """
    Display all business listings
    """
    category = request.GET.get("category", "")
    search_query = request.GET.get("q", "")

    listings = BusinessListing.objects.all()

    # Apply filters
    if category:
        listings = listings.filter(category=category)

    if search_query:
        listings = listings.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(city__icontains=search_query)
        )

    context = {
        "listings": listings,
        "categories": BusinessListing.CATEGORY_CHOICES,
        "selected_category": category,
        "search_query": search_query,
    }

    return render(request, "home/business_listing_list.html", context)


def business_listing_detail(request, slug):
    """
    Display details of a specific business listing
    """
    listing = get_object_or_404(BusinessListing, slug=slug)

    # Check if the current user has already submitted a claim request
    claim_request = None
    if request.user.is_authenticated:
        claim_request = ClaimRequest.objects.filter(
            business=listing, user=request.user
        ).first()

    context = {
        "listing": listing,
        "claim_request": claim_request,
    }

    return render(request, "home/business_listing_detail.html", context)


@login_required
def claim_business(request, slug):
    """
    Handle business claim requests
    """
    listing = get_object_or_404(BusinessListing, slug=slug)

    # Check if the business is already claimed
    if listing.is_claimed:
        messages.error(request, "This business has already been claimed.")
        return redirect("business_listing_detail", slug=slug)

    # Check if the user is a business user
    if request.user.user_type != "business":
        messages.error(request, "Only business accounts can claim business listings.")
        return redirect("business_listing_detail", slug=slug)

    # Check if the user has already submitted a claim request
    existing_request = ClaimRequest.objects.filter(
        business=listing, user=request.user
    ).exists()

    if existing_request:
        messages.info(
            request, "You have already submitted a claim request for this business."
        )
        return redirect("business_listing_detail", slug=slug)

    if request.method == "POST":
        form = ClaimRequestForm(request.POST, request.FILES)
        if form.is_valid():
            claim_request = form.save(commit=False)
            claim_request.business = listing
            claim_request.user = request.user
            claim_request.save()

            messages.success(
                request, "Your claim request has been submitted and is pending review."
            )
            return redirect("business_listing_detail", slug=slug)
    else:
        form = ClaimRequestForm()

    return render(
        request, "home/claim_business.html", {"listing": listing, "form": form}
    )


@login_required
def my_businesses(request):
    """
    Display businesses owned by the current user and claim requests
    """
    # Get businesses owned by the user
    owned_businesses = BusinessListing.objects.filter(owner=request.user)

    # Get claim requests made by the user
    claim_requests = ClaimRequest.objects.filter(user=request.user)

    context = {
        "owned_businesses": owned_businesses,
        "claim_requests": claim_requests,
    }

    return render(request, "home/my_businesses.html", context)


@login_required
def cancel_claim_request(request, pk):
    """
    Cancel a pending claim request
    """
    claim_request = get_object_or_404(ClaimRequest, pk=pk, user=request.user)

    if claim_request.status != "pending":
        messages.error(request, "You can only cancel pending claim requests.")
        return redirect("my_businesses")

    if request.method == "POST":
        claim_request.delete()
        messages.success(request, "Your claim request has been cancelled.")
        return redirect("my_businesses")

    return render(
        request, "home/cancel_claim_request.html", {"claim_request": claim_request}
    )


# edit delete business listing views
@login_required
def edit_business(request, slug):
    listing = get_object_or_404(BusinessListing, slug=slug)

    # Check if user is the owner
    if not listing.is_owner(request.user):
        return HttpResponseForbidden(
            "You don't have permission to edit this business profile"
        )

    if request.method == "POST":
        form = BusinessListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            business_profile = form.save()

            # Since this is now considered a profile, we might want to update user-related fields
            # For example, if you have fields that should be synchronized:
            # request.user.business_name = business_profile.name
            # request.user.save()

            messages.success(
                request, "Your business profile has been updated successfully."
            )
            return redirect("business_listing_detail", slug=business_profile.slug)
    else:
        form = BusinessListingForm(instance=listing)

    return render(
        request,
        "home/edit-business.html",
        {
            "form": form,
            "listing": listing,
            "is_profile": True,  # Flag to indicate this is a profile edit
        },
    )


@login_required
def delete_business(request, slug):
    listing = get_object_or_404(BusinessListing, slug=slug)

    # Check if user is the owner
    if not listing.is_owner(request.user):
        return HttpResponseForbidden(
            "You don't have permission to delete this business profile"
        )

    if request.method == "POST":
        listing_name = listing.name

        # Option 1: Delete the business listing but keep the user account
        listing.delete()
        messages.success(
            request, f"Your business profile '{listing_name}' has been deleted."
        )

        # Option 2: If you want to deactivate the user account as well
        # request.user.is_active = False
        # request.user.save()
        # messages.success(request, f"Your business profile '{listing_name}' and account have been deactivated.")
        # logout(request)

        return redirect("home")

    return render(
        request,
        "home/delete-business-confirm.html",
        {
            "listing": listing,
            "is_profile": True,  # Flag to indicate this is a profile deletion
        },
    )


@login_required
def approve_claim_request(request, pk):
    """
    Approve a claim request (admin only)
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to perform this action")

    claim_request = get_object_or_404(ClaimRequest, pk=pk)

    if claim_request.status != "pending":
        messages.error(request, "This claim request has already been processed.")
        return redirect("admin:home_claimrequest_changelist")

    if request.method == "POST":
        # Approve the claim and transfer ownership
        business = claim_request.approve()

        messages.success(
            request,
            f"Claim request approved. {business.name} is now owned by {claim_request.user.email}.",
        )
        return redirect("admin:home_claimrequest_changelist")

    return render(
        request, "admin/approve_claim_request.html", {"claim_request": claim_request}
    )
