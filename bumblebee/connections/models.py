from django.contrib.postgres.fields import ArrayField
from django.db import models

from bumblebee.users.models import CustomUser


# Create your models here.
class Follower(models.Model):
    """ """

    user = models.OneToOneField(
        CustomUser, related_name="user_follower", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    follower = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )
    requests_for_follow = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"

    def __str__(self) -> str:
        return f"{self.user.username} followers"


class Following(models.Model):
    """ """

    user = models.OneToOneField(
        CustomUser, related_name="user_following", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    following = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )
    requesting_to_follow = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        verbose_name = "Following"
        verbose_name_plural = "Followings"

    def __str__(self) -> str:
        return f"{self.user.username} followings"


class Muted(models.Model):
    """ """

    user = models.OneToOneField(
        CustomUser, related_name="user_muted", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    muted = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        verbose_name = "Muted Account"
        verbose_name_plural = "Muted Accounts"

    def __str__(self) -> str:
        return f"{self.user.username} muted accounts"


class Blocked(models.Model):
    """ """

    user = models.OneToOneField(
        CustomUser, related_name="user_blocked", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    blocked = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        verbose_name = "Blockaed Account"
        verbose_name_plural = "Blocked Accounts"

    def __str__(self) -> str:
        return f"{self.user.username} blocked accounts"
