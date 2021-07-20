from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Buzz


class BuzzAdminCreationForm(forms.ModelForm):

    image = forms.ImageField(
        required=False,
        max_length=8,
        help_text="Select Images. Maximum 8 allowed",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Buzz
        fields = ["author", "privacy", "content", "image", "location", "flair"]


class BuzzAdminForm(forms.ModelForm):

    image = forms.ImageField(
        required=False,
        max_length=8,
        help_text="Select Images. Maximum 8 allowed",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Buzz
        fields = ["author", "privacy", "content", "image", "location", "flair"]
