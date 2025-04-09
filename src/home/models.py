from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify


class BusinessListing(models.Model):
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

    PRICE_RANGE_CHOICES = (
        ("$", "Budget"),
        ("$$", "Moderate"),
        ("$$$", "Expensive"),
        ("$$$$", "Luxury"),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    price_range = models.CharField(
        max_length=10, choices=PRICE_RANGE_CHOICES, blank=True, null=True
    )
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    featured = models.BooleanField(default=False)
    is_claimed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="owned_businesses",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Listing"
        verbose_name_plural = "Business Listings"
        ordering = ["-featured", "-created_at"]

    def is_owner(self, user):
        return user.is_authenticated and self.owner == user

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

            # Ensure slug is unique
            original_slug = self.slug
            counter = 1
            while BusinessListing.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)


class ClaimRequest(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    business = models.ForeignKey(
        BusinessListing, on_delete=models.CASCADE, related_name="claim_requests"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="claim_requests",
    )
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Claim Request"
        verbose_name_plural = "Claim Requests"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Claim for {self.business.name} by {self.user.username}"
