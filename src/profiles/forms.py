from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from taggit.forms import TagWidget

from .models import Profile

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "user_type")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            '<a href="../password/">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "user_type",
            "slug",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class ProfileForm(forms.ModelForm):
    """
    Form for updating user profile information
    """

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = (
            "bio",
            "phone_number",
            "address",
            "district",
            "county",
            "sub_county",
            "parish",
            "village",
            "website",
            "twitter",
            "instagram",
            "facebook",
            "tags",
        )
        widgets = {
            "tags": TagWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)

        # Update the associated user's information
        user = profile.user
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.email = self.cleaned_data.get("email", "")

        if commit:
            user.save()
            profile.save()

        return profile


class CustomSignupForm(SignupForm):
    """
    Custom signup form for django-allauth that extends the default SignupForm
    """

    first_name = forms.CharField(max_length=30, label=_("First Name"), required=False)
    last_name = forms.CharField(max_length=30, label=_("Last Name"), required=False)
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        initial="customer",
        label=_("Account Type"),
        widget=forms.RadioSelect,
    )

    business_category = forms.ChoiceField(
        choices=User.CATEGORY_CHOICES,
        label=_("Business Category"),
        required=False,
        initial="other",
    )

    def save(self, request):
        # First call the parent class's save method to create the user
        user = super(CustomSignupForm, self).save(request)

        # Then update the additional fields
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.user_type = self.cleaned_data.get("user_type", "customer")
        # Set business category if user is a business
        if user.user_type == "business":
            user.business_category = self.cleaned_data.get("business_category", "other")
        user.save()

        return user
