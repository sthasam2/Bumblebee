from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


from bumblebee.activities.models import UserActivity
from bumblebee.activities.utils import _create_activity
from .models import Buzz, Rebuzz, BuzzInteractions, RebuzzInteractions


@receiver(post_save, sender=Buzz)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """ """

    if created:
        BuzzInteractions.objects.create(buzz=instance)
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
        _create_activity(
            instance.author,
            UserActivity.Actions.POST,
            ContentType.objects.get_for_model(instance),
            instance.id,
        )
