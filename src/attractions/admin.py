from django.contrib import admin

from .forms import AttractionAdminForm
from .models import Attraction


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    form = AttractionAdminForm
    list_display = ("name", "city", "category", "is_featured", "is_active")
    list_filter = ("category", "city", "is_featured", "is_active")
    search_fields = ("name", "description", "city__name")
    prepopulated_fields = {"slug": ("name",)}
