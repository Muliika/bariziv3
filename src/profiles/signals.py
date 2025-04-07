from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update a profile when a user is created or updated
    """
    # Use transaction.on_commit to ensure the user is saved before creating the profile
    transaction.on_commit(lambda: create_profile_if_needed(instance, created))


def create_profile_if_needed(user_instance, created):
    """
    Helper function to create a profile if it doesn't exist
    """
    try:
        # Try to access the profile
        profile = user_instance.profile
        if not created:  # If user was updated, not created
            profile.save()  # Update the profile
    except Profile.DoesNotExist:
        # If profile doesn't exist, create it
        Profile.objects.create(user=user_instance)
