from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from bumblebee.activities.models import UserActivity
from bumblebee.activities.utils import _create_activity
from bumblebee.notifications.models.grouped_models import (
    BuzzNotification,
    RebuzzNotification,
)

from .models import Buzz, BuzzInteractions, Rebuzz, RebuzzInteractions

#########################################
#           CONTENTS
#########################################


@receiver(post_save, sender=Buzz)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """ """

    if created:
        BuzzInteractions.objects.create(buzz=instance)
        BuzzNotification.objects.create(buzz=instance, user=instance.author)
        _create_activity(
            instance.author,
            UserActivity.Actions.POST,
            ContentType.objects.get_for_model(instance),
            instance.id,
        )


@receiver(post_save, sender=Rebuzz)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """ """

    if created:
        RebuzzInteractions.objects.create(rebuzz=instance)
        RebuzzNotification.objects.create(rebuzz=instance, user=instance.author)
        _create_activity(
            instance.author,
            UserActivity.Actions.POST,
            ContentType.objects.get_for_model(instance),
            instance.id,
        )


#########################################
#           INTERACTIONS
#########################################


# ACTIVITY


@receiver(post_save, sender=BuzzInteractions)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """ """

    # if created:
    #     RebuzzInteractions.objects.create(rebuzz=instance)
    #     _create_activity(
    #         instance.author,
    #         UserActivity.Actions.POST,
    #         ContentType.objects.get_for_model(instance),
    #         instance.id,
    #     )


@receiver(post_save, sender=RebuzzInteractions)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """ """

    # if created:
    #     RebuzzInteractions.objects.create(rebuzz=instance)
    #     _create_activity(
    #         instance.author,
    #         UserActivity.Actions.POST,
    #         ContentType.objects.get_for_model(instance),
    #         instance.id,
    #     )


# NOTIFICATIONS
