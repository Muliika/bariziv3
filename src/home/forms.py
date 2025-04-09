from django import forms

from .models import ClaimRequest


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
