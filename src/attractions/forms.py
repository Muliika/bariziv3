from django import forms

from cities.models import City

from .models import Attraction


class AttractionAdminForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure the city field is a proper ModelChoiceField
        self.fields["city"].queryset = City.objects.filter(is_active=True)
        self.fields["city"].widget.attrs.update({"class": "select2"})
