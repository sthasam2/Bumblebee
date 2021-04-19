from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from activities.models import UserActivity


from bumblebee.users.models import CustomUser
from bumblebee.activities.utils import _create_activity
from .models import Buzz, Comment, CommentInteractions, Interactions


@receiver(post_save, sender=Buzz)
def post_save_create_interaction_activity(sender, instance, created, **kwargs):
    """"""

    if created:
        Interactions.object.create(buzz=instance)
        _create_activity(
            Buzz.user,
            UserActivity.Actions.POST,
            ContentType.objects.get_for_model(instance),
            instance.id,
        )
