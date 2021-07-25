from django.contrib.postgres.fields import ArrayField
from django.db import models

from bumblebee.buzzes.models import Buzz, Rebuzz
from bumblebee.users.models import CustomUser
from bumblebee.notifications.utils import generate_notification_string

# Create your models here.
class BaseNotification(models.Model):
    """ """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_add=True)

    class Meta:
        abstract = True


#########################################
#           BUZZ
#########################################


class BuzzUpvotedNotification(BaseNotification):
    """ """

    buzz = models.OneToOneField(
        Buzz, related_name="buzz_upvote_notification", on_delete=models.CASCADE
    )
    latest = ArrayField(
        models.models.CharField(max_length=100), blank=True, default=list
    )
    upvoted = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        verbose_name = "Buzz Upvote Notification"

    def __str__(self):
        return generate_notification_string("upvoted", self.upvoted, "buzz")


class BuzzDownvotedNotification(BaseNotification):
    """ """

    buzz = models.OneToOneField(
        Buzz, related_name="buzz_upvote_notification", on_delete=models.CASCADE
    )
    latest = ArrayField(
        models.models.CharField(max_length=100), blank=True, default=list
    )
    downvoted = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        verbose_name = "Buzz Downvote Notification"

    def __str__(self):
        return generate_notification_string("downvoted", self.downvoted, "buzz")


class BuzzRebuzzedNotification(BaseNotification):
    """ """

    buzz = models.OneToOneField(
        Buzz, related_name="buzz_upvote_notification", on_delete=models.CASCADE
    )
    latest = ArrayField(
        models.models.CharField(max_length=100), blank=True, default=list
    )
    rebuzzed = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        verbose_name = "Buzz Rebuzz Notification"

    def __str__(self):
        return generate_notification_string("rebuzzed", self.rebuzzed, "buzz")


class BuzzCommentedNotification(BaseNotification):
    """ """

    buzz = models.OneToOneField(
        Buzz, related_name="buzz_upvote_notification", on_delete=models.CASCADE
    )
    latest = ArrayField(
        models.models.CharField(max_length=100), blank=True, default=list
    )
    commented = ArrayField(
        models.PositiveIntegerField(blank=False), blank=True, default=list
    )

    class Meta:
        verbose_name = "Buzz Comment Notification"

    def __str__(self):
        return generate_notification_string("commented on", self.commented, "buzz")


#########################################
#           REBUZZ
#########################################
