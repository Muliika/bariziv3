from django.core.management.base import BaseCommand

from profiles.models import Profile, User


class Command(BaseCommand):
    help = "Creates missing profiles for users"

    def handle(self, *args, **options):
        users_without_profiles = []

        for user in User.objects.all():
            try:
                # Try to access the profile
                user.profile
            except:
                # If profile doesn't exist, add user to the list
                users_without_profiles.append(user)

        if not users_without_profiles:
            self.stdout.write(self.style.SUCCESS("All users have profiles!"))
            return

        # Create profiles for users without them
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(f"Created profile for user: {user.username}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(users_without_profiles)} missing profiles"
            )
        )
