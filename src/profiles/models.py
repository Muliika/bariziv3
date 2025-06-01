from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager where both email and username are unique identifiers
    that can be used for authentication.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and save a user with the given email, username and password.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))
        if not username:
            raise ValueError(_("Users must have a username"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email, username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses both email and username as unique identifiers
    for authentication.
    """

    CATEGORY_CHOICES = (
        ("accommodation", "Accommodation"),
        ("food_drinks", "Food & Drinks"),
        ("activities", "Activities"),
        ("shopping", "Shopping"),
        ("health", "Health"),
        ("entertainment", "Entertainment"),
        ("services", "Services"),
        ("other", "Other"),
    )

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    # You can add additional fields here
    USER_TYPE_CHOICES = [
        ("customer", "Customer"),
        ("business", "Business"),
        # ("admin", "Admin"),
    ]
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="customer"
    )
    business_category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="other", blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"  # Primary identifier for Django authentication
    EMAIL_FIELD = "email"  # Used by Django for sending emails
    REQUIRED_FIELDS = ["email"]  # Required when creating a user via createsuperuser

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() or self.username

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name or self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Profile(models.Model):
    """
    User profile with additional information
    """

    PRICE_RANGE_CHOICES = (
        ("$", "Budget"),
        ("$$", "Moderate"),
        ("$$$", "Expensive"),
        ("$$$$", "Luxury"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # profile_picture = models.ImageField(
    #     upload_to="profile_pics/", blank=True, null=True
    # )
    bio = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    district = models.CharField(
        max_length=100, blank=True, null=True, default="Kampala"
    )
    county = models.CharField(max_length=100, blank=True, null=True, default=" ")
    sub_county = models.CharField(max_length=100, blank=True, null=True, default=" ")
    parish = models.CharField(max_length=100, blank=True, null=True, default=" ")
    village = models.CharField(max_length=100, blank=True, null=True, default=" ")

    # Social media accounts
    website = models.URLField(max_length=200, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    featured = models.BooleanField(default=False)

    price_range = models.CharField(
        max_length=10, choices=PRICE_RANGE_CHOICES, blank=True, null=True
    )
    tags = TaggableManager(
        blank=True, help_text="A comma-separated list of tags for your profile"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Bookmark(models.Model):
    """
    Model to store user bookmarks for listings
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    listing_id = models.IntegerField()  # Reference to the listing
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "listing_id")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - Listing {self.listing_id}"
