from django.db import models
from django.utils.text import slugify


class District(models.Model):
    """Model representing a district in Uganda"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    population = models.PositiveIntegerField(blank=True, null=True)
    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Area in square kilometers",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "District"
        verbose_name_plural = "Districts"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class City(models.Model):
    """Model representing a city or town in Uganda"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="cities"
    )

    # City details
    description = models.TextField(blank=True, null=True)
    population = models.PositiveIntegerField(blank=True, null=True)
    is_capital = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    # Location information
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )

    # Media
    image = models.ImageField(upload_to="cities/images/", blank=True, null=True)

    # Meta information
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = [
            "name",
            "district",
        ]  # City names can repeat but not in the same district

    def __str__(self):
        return f"{self.name}, {self.district.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.district.name}")
        super().save(*args, **kwargs)


class CityAttraction(models.Model):
    """Model representing tourist attractions in a city"""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="attractions")
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
        ordering = ["name"]
        verbose_name = "City Attraction"
        verbose_name_plural = "City Attractions"

    def __str__(self):
        return f"{self.name} - {self.city.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.city.name}")
        super().save(*args, **kwargs)
