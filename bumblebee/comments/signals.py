from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


from bumblebee.activities.models import UserActivity
from bumblebee.activities.utils import _create_activity

from .models import Comment, CommentInteractions


@receiver(post_save, sender=Comment)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """"""

    if created:
        CommentInteractions.object.create(buzz=instance)
        _create_activity(
            instance.user,
            UserActivity.Actions.COMMENT,
            ContentType.objects.get_for_model(instance),
            instance.id,
        )
