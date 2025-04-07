from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm
from .models import Profile


@login_required
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
