import uuid as _uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from bumblebee.users.managers import CustomUserManager
from django.db.models.signals import post_save


class CustomUser(AbstractBaseUser):
    """
    Custom extension of the AbstractBaseUser to create a custom user field
    """

    uuid = models.UUIDField(primary_key=True, default=_uuid.uuid5, editable=False)

    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=False,
        help_text="Username. example: sam_smith",
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        help_text="Email address. example: example@example.domain",
    )
    registered_date = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)

    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return self.email

    def _send_verification_mail(self):
        pass

    def get_username(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_email_verified(self):
        return self.email_verified
