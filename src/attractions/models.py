from django.db import models

from cities.models import City


class Attraction(models.Model):
    """Model representing tourist attractions"""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="city_attractions"
    )
    description = models.TextField()

    # Categories for attractions
    CATEGORY_CHOICES = [
        ("natural", "Natural Attraction"),
        ("historical", "Historical Site"),
        ("cultural", "Cultural Venue"),
        ("entertainment", "Entertainment"),
        ("shopping", "Shopping"),
        ("food", "Food & Dining"),
        ("other", "Other"),
    ]
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )

    # Contact and location details
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Media
    image = models.ImageField(upload_to="attractions/images/", blank=True, null=True)

    # Meta information
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attraction"
        verbose_name_plural = "Attractions"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.city.name}"

    def save(self, *args, **kwargs):
        from django.utils.text import slugify

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
