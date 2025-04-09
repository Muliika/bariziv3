from django import forms

from .models import ClaimRequest


class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ["proof_document", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "proof_document": forms.FileInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "proof_document": "Upload a document that proves you are the owner of this business (e.g., business license, utility bill, etc.)",
            "notes": "Provide any additional information that might help us verify your ownership of this business.",
        }
