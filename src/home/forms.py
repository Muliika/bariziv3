from django import forms

from .models import BusinessListing, ClaimRequest


class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ["notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
        help_texts = {
            "notes": "Provide any additional information that might help us verify your ownership of this business.",
        }


class BusinessListingForm(forms.ModelForm):
    class Meta:
        model = BusinessListing
        fields = [
            "name",
            "category",
            "description",
            "address",
            "city",
            "phone",
            "email",
            "website",
            # Add any other fields that should be editable
        ]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "opening_hours": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            # Add more widget customizations as needed
        }
