from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from bumblebee.users.models import CustomUser


class UserActivity(models.Model):
    """
    Model for user activities
    """

    class Actions(models.TextChoices):
        # user
        SIGN_UP = "sgu", "signed up"
        LOG_IN = "lgn", "logged in"
        RESET_PW = "rstpw", "reset password"
        DEACTIVATE = "deac", "deactivated"
        DELETE = "del", "deleted"
        # profile
        VIEW = "vw", "viewed"
        UPDATE = "upd", "updated"
        # buzz
        POST = "pst", "posted"
        UPVOTE = "upv", "upvoted"
        DOWNVOTE = "dwv", "downvoted"
        CREATE = "crt", "created"
        COMMENT = "cmt", "commented"
        EDIT = "edt", "edited"
        # follow
        UNFOLLOW = "unflw", "unfollowed"
        FOLLOW = "flw", "followed"
        REQUEST = "req", "requested"

    user = models.ForeignKey(
        CustomUser,
        related_name="useractivity",
        db_index=True,
        on_delete=models.CASCADE,
    )

    action = models.CharField(
        max_length=250, choices=Actions.choices
    )  # the action of the user

    target_content = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_object",
        on_delete=models.CASCADE,
    )  # the target object
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ("-created_date",)

    # def create_activity():

    def __str__(self):
        return f"{self.user} {self.action} {self.target_content}:{self.target_id}"
