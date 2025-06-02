# from django.contrib import admin

# from .models import City, CityAttraction, District


# @admin.register(District)
# class DistrictAdmin(admin.ModelAdmin):
#     list_display = ("name", "population", "is_active")
#     list_filter = ("is_active",)
#     search_fields = ("name", "description")
#     prepopulated_fields = {"slug": ("name",)}


# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "district",
#         "population",
#         "is_capital",
#         "is_featured",
#         "is_active",
#     )
#     list_filter = ("district", "is_capital", "is_featured", "is_active")
#     search_fields = ("name", "description", "district__name")
#     prepopulated_fields = {"slug": ("name",)}


# @admin.register(CityAttraction)
# class CityAttractionAdmin(admin.ModelAdmin):
#     list_display = ("name", "city", "category", "is_featured", "is_active")
#     list_filter = ("category", "city", "is_featured", "is_active")
#     search_fields = ("name", "description", "city__name")
#     prepopulated_fields = {"slug": ("name",)}

from django.contrib import admin

from .models import City, CityAttraction, District  # Make sure to import all models


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "is_capital", "is_featured", "is_active")
    list_filter = ("district", "is_capital", "is_featured", "is_active")
    search_fields = ("name", "description", "district__name")
    prepopulated_fields = {"slug": ("name",)}

    # This is important for the autocomplete to work
    search_fields = ["name"]


# Make sure your other models are registered too
@admin.register(CityAttraction)
class CityAttractionAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "category", "is_featured", "is_active")
    list_filter = ("category", "city", "is_featured", "is_active")
    search_fields = ("name", "description", "city__name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
