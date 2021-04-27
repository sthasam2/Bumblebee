from django.core.validators import RegexValidator
from django.db import models
from django.db.models.deletion import CASCADE

from bumblebee.users.models import CustomUser
from .validators import validate_date_lt_today


class Profile(models.Model):
    """"""

    user = models.OneToOneField(
        CustomUser, related_name="profile", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    account_verified = models.BooleanField(default=False)

    avatar = models.ImageField(default="default.png", upload_to="avatar/")
    cover = models.ImageField(default="default.png", upload_to="cover/")

    bio = models.CharField(max_length=200)
    name = models.CharField(
        name="Name",
        max_length=747,
        unique=False,
        help_text="Full Name. For eg. Will Smith ",
    )
    nickname = models.CharField(
        name="Nickname",
        max_length=50,
        unique=False,
        help_text="Nickname. The name you want to be called. For eg. Will",
    )
    dob = models.DateTimeField(
        name="DOB",
        validators=[validate_date_lt_today],
        null=True,
        unique=False,
        blank=True,
    )
    location = models.CharField(
        name="Location",
        max_length=200,
        help_text="User Location. Street, Municipality/VDC, State, Country",
    )

    phone_validator = RegexValidator(
        regex=r"^\+?1?\d{9,14}$",
        message="Phone number. It must contain Dialing code and contact number. For eg. +977980000000000",
    )
    phone = models.CharField(
        name="Phone",
        validators=[phone_validator],
        max_length=17,
        unique=True,
        blank=True,
        null=True,
    )
    phone_verified = models.BooleanField(name="Contact number verified", default=False)

    # def __init__(self, *args, **kwargs):
    #     """
    #     Overriding init method
    #     """
    #     super(Profile, self).__init__(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     """
    #     Overriding default save method
    #     """
    #     super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Profile"

    def get_username(self):
        return self.user.username

    def get_fullname(self):
        return self.name

    def get_shortname(self):
        return self.nickname

    def is_account_verified(self):
        return self.account_verified
