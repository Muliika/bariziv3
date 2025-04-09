from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import BusinessListing, ClaimRequest


@admin.register(BusinessListing)
class BusinessListingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "city",
        "rating",
        "featured",
        "is_claimed",
        "is_verified",
        "owner",
    )
    list_filter = ("category", "featured", "is_claimed", "is_verified", "city")
    search_fields = ("name", "description", "address", "city")
    prepopulated_fields = {"slug": ("name",)}
    actions = ["mark_as_featured", "mark_as_verified"]

    def mark_as_featured(self, request, queryset):
        queryset.update(featured=True)

    mark_as_featured.short_description = "Mark selected listings as featured"

    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)

    mark_as_verified.short_description = "Mark selected listings as verified"


@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ("business", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("business__name", "user__username", "user__email")
    actions = ["approve_claims", "reject_claims"]

    # def approve_claims(self, request, queryset):
    #     for claim in queryset.filter(status="pending"):
    #         # Update the claim status
    #         claim.status = "approved"
    #         claim.save()

    #         # Update the business
    #         business = claim.business
    #         business.is_claimed = True
    #         business.owner = claim.user
    #         business.save()

    # approve_claims.short_description = "Approve selected claim requests"
    def admin_actions(self, obj):
        """Custom column to add action buttons for each claim request"""
        if obj.status == "pending":
            approve_url = reverse("approve_claim_request", args=[obj.pk])
            return format_html(
                '<a href="{}" class="button" style="background-color: #28a745; color: white; '
                'padding: 5px 10px; text-decoration: none; border-radius: 4px; margin-right: 5px;">'
                '<i class="fas fa-check"></i> Approve</a>',
                approve_url,
            )
        return "-"

    admin_actions.short_description = "Actions"

    # def approve_claims(self, request, queryset):
    #     for claim in queryset:
    #         business = claim.business
    #         business.is_claimed = True
    #         business.owner = claim.user  # Set the owner to the user who claimed it
    #         business.save()
    #         claim.status = "approved"
    #         claim.save()
    #     self.message_user(
    #         request, f"{queryset.count()} claim requests approved successfully."
    #     )
    def approve_claims(self, request, queryset):
        for claim in queryset.filter(status="pending"):
            # Update the business first
            business = claim.business
            business.is_claimed = True
            business.owner = claim.user  # Set the owner to the user who claimed it
            business.save()

            # Then update the claim status
            claim.status = "approved"
            claim.save()

        self.message_user(
            request, f"{queryset.count()} claim requests approved successfully."
        )

    approve_claims.short_description = "Approve selected claim requests"

    def reject_claims(self, request, queryset):
        queryset.filter(status="pending").update(status="rejected")

    reject_claims.short_description = "Reject selected claim requests"
