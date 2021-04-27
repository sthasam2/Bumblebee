from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


from bumblebee.activities.models import UserActivity
from bumblebee.activities.utils import _create_activity
from bumblebee.users.models import CustomUser
from .models import Buzz, Rebuzz, BuzzInteractions


@receiver(post_save, sender=Buzz)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """"""

    if created:
        BuzzInteractions.objects.create(buzz=instance)
        _create_activity(
            instance.user,
            UserActivity.Actions.POST,
            ContentType.objects.get_for_model(instance),
            instance.id,
        )


@receiver(post_save, sender=Rebuzz)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """"""

    if created:
        BuzzInteractions.objects.create(buzz=instance)
        _create_activity(
            instance.user,
            UserActivity.Actions.POST,
            ContentType.objects.get_for_model(instance),
            instance.id,
        )
