from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


# Define a validator for Pakistani mobile numbers
pakistani_mobile_validator = RegexValidator(
    regex=r"^(?:\+92|0)3\d{9}$",
    message="Enter a valid Pakistani mobile number, e.g., +923362108399 or 03362108399",
)


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    mobile_number = forms.CharField(
        max_length=15,
        required=True,
        label="Mobile Number",
        validators=[pakistani_mobile_validator],  # Add the validator here
        widget=forms.TextInput(
            attrs={"placeholder": "Mobile Number"},
        ),  # Add placeholder here
    )

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super().save(request)

        # Add your own processing here.
        user.mobile_number = self.cleaned_data["mobile_number"]
        user.save()

        # You must return the original result.
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
